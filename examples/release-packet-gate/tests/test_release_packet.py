import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import release_packet


class ReleasePacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = ROOT / "examples"
        cls.now = datetime(2026, 9, 25, 8, 0, tzinfo=timezone.utc)
        cls.decision = release_packet.digest(cls.base / "decision.txt")
        cls.artifact = release_packet.digest(cls.base / "artifact.txt")

    def packet(self):
        report = {
            "status": "PASS",
            "issuer": "protected-ci-app",
            "decision_sha256": self.decision,
            "artifact_sha256": self.artifact,
            "observed_at": "2026-09-25T07:30:00Z",
        }
        return {
            "phase": "promotion",
            "decision_file": "decision.txt",
            "artifact_file": "artifact.txt",
            "expected_issuer": "protected-ci-app",
            "max_age_hours": 2,
            "required_cohort": "migration-001-and-nonentitled-control",
            "evidence": {
                "intent": dict(report),
                "behavior": dict(report),
                "operation": dict(report, cohort="migration-001-and-nonentitled-control"),
            },
        }

    def verdict(self, packet):
        return release_packet.evaluate(packet, self.base, self.now)

    def test_all_three_current_rails_pass(self):
        self.assertEqual(self.verdict(self.packet())["overall"], "PASS")

    def test_measured_failure_vetoes(self):
        packet = self.packet()
        packet["evidence"]["behavior"]["status"] = "FAIL"
        self.assertEqual(self.verdict(packet)["overall"], "FAIL")

    def test_missing_operation_is_unverified_at_promotion(self):
        packet = self.packet()
        del packet["evidence"]["operation"]
        self.assertEqual(self.verdict(packet)["overall"], "UNVERIFIED")

    def test_wrong_artifact_is_unverified(self):
        packet = self.packet()
        packet["evidence"]["behavior"]["artifact_sha256"] = "0" * 64
        self.assertEqual(self.verdict(packet)["rails"]["behavior"]["reason"], "artifact digest mismatch")

    def test_stale_report_is_unverified(self):
        packet = self.packet()
        packet["evidence"]["behavior"]["observed_at"] = "2026-09-24T01:00:00Z"
        self.assertEqual(self.verdict(packet)["rails"]["behavior"]["reason"], "stale or future evidence")

    def test_wrong_cohort_is_unverified(self):
        packet = self.packet()
        packet["evidence"]["operation"]["cohort"] = "all-other-tenants"
        self.assertEqual(self.verdict(packet)["rails"]["operation"]["reason"], "wrong or absent customer cohort")

    def test_unrecognized_issuer_is_unverified(self):
        packet = self.packet()
        packet["evidence"]["intent"]["issuer"] = "coding-worker"
        self.assertEqual(self.verdict(packet)["rails"]["intent"]["reason"], "unrecognized report issuer")

    def test_prelaunch_does_not_require_operation(self):
        packet = self.packet()
        packet["phase"] = "prelaunch"
        del packet["evidence"]["operation"]
        self.assertEqual(self.verdict(packet)["overall"], "PASS")


if __name__ == "__main__":
    unittest.main()
