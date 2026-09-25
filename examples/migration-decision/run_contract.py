"""Require a green normal contract and red deliberate faults.

The local JSON report is only a dry-run receipt. It is not evidence that this
fictional policy matches any real organization or that a live route was tested.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
CASES = ("", "accept_every_true", "new_key_on_retry")
EXPECTED_TESTS = 2


def main() -> None:
    observed = []
    for mutation in CASES:
        env = os.environ.copy()
        env["FIELD_NOTES_MUTATION"] = mutation
        run = subprocess.run(
            [sys.executable, "-m", "unittest", "trusted_contract", "-v"],
            cwd=HERE, env=env, capture_output=True, text=True,
        )
        count_match = re.search(r"(?m)^Ran (\d+) tests? in ", run.stderr)
        test_count = int(count_match.group(1)) if count_match else 0
        if test_count != EXPECTED_TESTS:
            raise SystemExit(
                f"Contract collected {test_count} tests for {mutation or 'normal'}; "
                f"expected {EXPECTED_TESTS}.\n{run.stderr[-1200:]}"
            )
        expected_pass = mutation == ""
        observed.append({
            "case": mutation or "normal",
            "contract_passed": run.returncode == 0,
            "expected_pass": expected_pass,
            "test_count": test_count,
        })
        print(f"{mutation or 'normal'}: {'GREEN' if run.returncode == 0 else 'RED'}")
        if (run.returncode == 0) != expected_pass:
            print(run.stderr[-1200:], file=sys.stderr)
            raise SystemExit(f"Contract did not react as expected: {mutation or 'normal'}")
    report = {
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "synthetic SQLite illustration, no production system",
        "observed": observed,
    }
    reports = HERE / "reports"
    reports.mkdir(exist_ok=True)
    (reports / "latest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Normal behavior passed; both selected negative controls failed as intended.")


if __name__ == "__main__":
    main()
