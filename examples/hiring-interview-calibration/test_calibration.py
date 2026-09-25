"""Negative controls for the synthetic reviewer-calibration example."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("calibrate_reviewers", HERE / "calibrate_reviewers.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class CalibrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.packet = json.loads((HERE / "reviewer-example.json").read_text(encoding="utf-8"))

    def inspect(self, packet: dict) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.json"
            path.write_text(json.dumps(packet), encoding="utf-8")
            return MODULE.inspect(path)

    def test_deliberate_disagreement_requests_calibration(self) -> None:
        self.assertEqual(self.inspect(self.packet), ["independent_verification: 4 versus 2"])

    def test_missing_dimension_is_rejected(self) -> None:
        del self.packet["reviewers"][0]["scores"]["technical_fundamentals"]
        with self.assertRaisesRegex(ValueError, "Incomplete dimensions"):
            self.inspect(self.packet)

    def test_empty_behavioral_evidence_is_rejected(self) -> None:
        self.packet["reviewers"][1]["scores"]["architecture_ownership"]["evidence"] = "sounds good"
        with self.assertRaisesRegex(ValueError, "too vague"):
            self.inspect(self.packet)

    def test_real_candidate_identifier_is_rejected(self) -> None:
        self.packet["candidate"] = "real-person"
        with self.assertRaisesRegex(ValueError, "synthetic example"):
            self.inspect(self.packet)


if __name__ == "__main__":
    unittest.main()
