"""Acceptance and negative controls for a fictional completed-run ledger."""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from contract_report import parse, report  # noqa: E402


class ContractReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = parse(ROOT / "sample-runs.csv")

    def test_retry_cost_reverses_sticker_price(self) -> None:
        result = report(self.rows)
        self.assertEqual(result["LowSticker"]["completed_cohort_cost_per_accepted_usd"], "27.00")
        self.assertEqual(result["FitForJob"]["completed_cohort_cost_per_accepted_usd"], "17.50")
        self.assertEqual(result["LowSticker"]["topology_mismatched_attempts"], 1)
        self.assertEqual(result["FitForJob"]["topology_mismatched_attempts"], 0)

    def test_two_successes_for_one_request_are_rejected(self) -> None:
        self.rows[0]["accepted"] = True
        with self.assertRaisesRegex(ValueError, "More than one accepted"):
            report(self.rows)

    def test_open_request_withholds_unit_cost(self) -> None:
        for row in self.rows:
            if row["request_id"] == "L-002":
                row["request_state"] = "open"
                row["accepted"] = False
        result = report(self.rows)["LowSticker"]
        self.assertEqual(result["open_requests"], 1)
        self.assertIsNone(result["completed_cohort_cost_per_accepted_usd"])
        self.assertEqual(result["observed_billed_usd"], "54.00")

    def test_queue_sum_is_not_a_first_start_sla_verdict(self) -> None:
        self.rows[0]["queue_minutes"] += 100
        result = report(self.rows)["LowSticker"]
        self.assertEqual(result["first_start_sla_verdict"], "not_measured")
        self.assertEqual(result["p95_sum_of_queue_intervals_minutes"], "129.90")
        self.assertNotIn("promised_start_misses", result)

    def test_conflicting_request_contract_is_rejected(self) -> None:
        self.rows[1]["requested_topology"] = "other-class"
        with self.assertRaisesRegex(ValueError, "Conflicting request contract"):
            report(self.rows)

    def test_duplicate_attempt_identity_is_rejected_at_ingest(self) -> None:
        with (ROOT / "sample-runs.csv").open(newline="", encoding="utf-8") as handle:
            raw = list(csv.DictReader(handle))
        raw.append(dict(raw[0]))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "duplicate.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(raw[0]))
                writer.writeheader()
                writer.writerows(raw)
            with self.assertRaisesRegex(ValueError, "Duplicate provider/attempt"):
                parse(path)


if __name__ == "__main__":
    unittest.main()
