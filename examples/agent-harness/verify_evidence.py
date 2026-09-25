#!/usr/bin/env python3
"""Independent CI check: normal suite, deliberate fault and WAL receipts.

Run outside the agent's writable worktree. JUnit reports and the expected
successful tool IDs must come from the trusted CI/runner.
"""
from __future__ import annotations
import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

def counts(path: Path) -> tuple[int, int, int]:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall(".//testsuite")
    if not suites:
        raise ValueError(f"{path.name}: no testsuite")
    tests = sum(int(s.get("tests", "0")) for s in suites)
    failures = sum(int(s.get("failures", "0")) + int(s.get("errors", "0")) for s in suites)
    skipped = sum(int(s.get("skipped", "0")) for s in suites)
    return tests, failures, skipped

def check(normal: Path, fault: Path, wal: Path, expected_ids: Path, run_id: str,
          run_start_utc: datetime) -> None:
    for report in (normal, fault):
        modified = datetime.fromtimestamp(report.stat().st_mtime, timezone.utc)
        if modified < run_start_utc:
            raise ValueError(f"{report.name}: report predates this CI run")
    tests, failures, skipped = counts(normal)
    if tests - skipped < 1 or failures:
        raise ValueError("normal run has no executed passing tests or has failures")
    tests, failures, skipped = counts(fault)
    if tests - skipped < 1 or failures < 1:
        raise ValueError("deliberate fault survived or no tests executed")
    ids = json.loads(expected_ids.read_text(encoding="utf-8"))
    if not isinstance(ids, list) or not ids or any(not isinstance(x, str) for x in ids):
        raise ValueError("trusted tool ID list is empty or invalid")
    receipts = [json.loads(line) for line in wal.read_text(encoding="utf-8").splitlines() if line.strip()]
    observed = {x["tool_use_id"] for x in receipts if x.get("run_id") == run_id}
    missing = sorted(set(ids) - observed)
    if missing:
        raise ValueError(f"WAL missing {len(missing)} expected tool receipts")

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--normal", type=Path, required=True)
    p.add_argument("--deliberate-fault", type=Path, required=True)
    p.add_argument("--wal", type=Path, required=True)
    p.add_argument("--expected-ids", type=Path, required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--run-start-utc", required=True, help="Trusted CI start time in ISO 8601")
    a = p.parse_args()
    try:
        start = datetime.fromisoformat(a.run_start_utc.replace("Z", "+00:00"))
        if start.tzinfo is None:
            raise ValueError("run start needs a timezone")
        check(a.normal, a.deliberate_fault, a.wal, a.expected_ids, a.run_id,
              start.astimezone(timezone.utc))
    except (OSError, ValueError, ET.ParseError, KeyError, TypeError) as exc:
        print(f"UNVERIFIED: {exc}", file=sys.stderr)
        return 1
    print("PASS: normal tests ran, deliberate fault failed, WAL receipts present")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
