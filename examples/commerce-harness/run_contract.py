"""Run normal tests and a deliberate mutant; fail unless normal is green and mutant red."""
from __future__ import annotations

import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPORTS = HERE / "reports"


def run(name: str, mutant: bool) -> tuple[subprocess.CompletedProcess, list[bool]]:
    env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    if mutant:
        env["COMMERCE_MUTANT"] = "1"
    else:
        env.pop("COMMERCE_MUTANT", None)
    report = REPORTS / (name + ".xml")
    started_ns = time.time_ns()
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(HERE / "trusted_contract.py"),
         f"--junitxml={report}"],
        cwd=HERE, env=env, capture_output=True, text=True,
    )
    if not report.exists() or report.stat().st_mtime_ns < started_ns:
        raise RuntimeError(f"{name}: missing or stale CI report")
    cases = ET.parse(report).getroot().findall(".//testcase")
    if {case.get("name") for case in cases} != {
        "test_last_unit_and_repeated_intent", "test_lost_ack_reuses_key_and_late_retry_reconciles"
    } or any(case.find("skipped") is not None for case in cases):
        raise RuntimeError(f"{name}: expected business tests did not execute")
    return result, [case.find("failure") is not None or case.find("error") is not None for case in cases]


def main() -> int:
    REPORTS.mkdir(exist_ok=True)
    normal, normal_failures = run("normal", False)
    print(normal.stdout, end="")
    if normal.returncode or any(normal_failures):
        print("FAIL: normal contract is red", file=sys.stderr)
        return 1
    mutant, mutant_failures = run("deliberate-fault", True)
    print(mutant.stdout, end="")
    if mutant.returncode == 0 or not all(mutant_failures):
        print("UNVERIFIED: deliberate fault survived", file=sys.stderr)
        return 1
    print("PASS: 2 normal contracts green; both deliberate faults red")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
