"""Evaluate a fictional three-rail release packet without network or effects."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RAILS = ("intent", "behavior", "operation")
PHASES = {"prelaunch": RAILS[:2], "promotion": RAILS}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp requires timezone")
    return parsed.astimezone(timezone.utc)


def evaluate(packet: dict[str, Any], base: Path, now: datetime) -> dict[str, Any]:
    phase = packet["phase"]
    if phase not in PHASES:
        raise ValueError(f"unknown phase: {phase}")
    if now.tzinfo is None:
        raise ValueError("now requires timezone")
    decision_path = base / packet["decision_file"]
    artifact_path = base / packet["artifact_file"]
    decision_sha = digest(decision_path)
    artifact_sha = digest(artifact_path)
    expected_issuer = packet["expected_issuer"]
    max_age_hours = float(packet["max_age_hours"])
    if max_age_hours <= 0:
        raise ValueError("max_age_hours must be positive")
    evidence = packet["evidence"]
    by_rail: dict[str, dict[str, str]] = {}
    for rail in PHASES[phase]:
        report = evidence.get(rail)
        if report is None:
            by_rail[rail] = {"state": "UNVERIFIED", "reason": "missing report"}
            continue
        if report.get("status") == "FAIL":
            by_rail[rail] = {"state": "FAIL", "reason": "measured claim failed"}
            continue
        if report.get("status") != "PASS":
            by_rail[rail] = {"state": "UNVERIFIED", "reason": "no positive measurement"}
            continue
        if report.get("issuer") != expected_issuer:
            by_rail[rail] = {"state": "UNVERIFIED", "reason": "unrecognized report issuer"}
            continue
        if report.get("decision_sha256") != decision_sha:
            by_rail[rail] = {"state": "UNVERIFIED", "reason": "decision digest mismatch"}
            continue
        if report.get("artifact_sha256") != artifact_sha:
            by_rail[rail] = {"state": "UNVERIFIED", "reason": "artifact digest mismatch"}
            continue
        try:
            observed = parse_time(report["observed_at"])
        except (KeyError, TypeError, ValueError):
            by_rail[rail] = {"state": "UNVERIFIED", "reason": "invalid observation time"}
            continue
        age_hours = (now.astimezone(timezone.utc) - observed).total_seconds() / 3600
        if not 0 <= age_hours <= max_age_hours:
            by_rail[rail] = {"state": "UNVERIFIED", "reason": "stale or future evidence"}
            continue
        if rail == "operation" and report.get("cohort") != packet.get("required_cohort"):
            by_rail[rail] = {"state": "UNVERIFIED", "reason": "wrong or absent customer cohort"}
            continue
        by_rail[rail] = {"state": "PASS", "reason": "packet conditions met"}
    states = [item["state"] for item in by_rail.values()]
    overall = "FAIL" if "FAIL" in states else ("UNVERIFIED" if "UNVERIFIED" in states else "PASS")
    return {
        "phase": phase,
        "overall": overall,
        "decision_sha256": decision_sha,
        "artifact_sha256": artifact_sha,
        "rails": by_rail,
        "limitations": "Local issuer strings are illustrative, not authenticated CI identity.",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python release_packet.py packet.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).resolve()
    packet = json.loads(path.read_text(encoding="utf-8"))
    now = parse_time(packet["as_of"])
    report = evaluate(packet, path.parent, now)
    print(json.dumps(report, indent=2))
    return {"PASS": 0, "FAIL": 1, "UNVERIFIED": 3}[report["overall"]]


if __name__ == "__main__":
    raise SystemExit(main())
