"""Acceptance checks for the disposable tenant fixture and its oracle."""
import unittest

from probes import one, suite


class TenantBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = suite()

    def test_positive_control_proves_receipt_sensor(self):
        row = self.rows[0]
        self.assertEqual("PASS", row["verdict"])
        self.assertEqual(1, row["actual_receipt_count"])
        self.assertNotEqual(row["target_sha_before"], row["target_sha_after"])

    def test_direct_denial_has_no_effect(self):
        row = self.rows[1]
        self.assertEqual("deny", row["hook_decision"])
        self.assertEqual("not_dispatched", row["service_verdict"])
        self.assertEqual("PASS", row["verdict"])

    def test_hook_crash_reaches_service_but_service_denies(self):
        row = self.rows[2]
        self.assertEqual("error:crash", row["hook_decision"])
        self.assertEqual("denied", row["service_verdict"])
        self.assertEqual("PASS", row["verdict"])

    def test_malformed_hook_result_is_not_permission(self):
        row = self.rows[3]
        self.assertEqual("denied", row["service_verdict"])
        self.assertEqual("PASS", row["verdict"])

    def test_timeout_is_not_permission(self):
        row = self.rows[4]
        self.assertEqual("denied", row["service_verdict"])
        self.assertEqual("PASS", row["verdict"])

    def test_missing_worker_hook_is_not_permission(self):
        row = self.rows[5]
        self.assertEqual("missing_worker", row["route"])
        self.assertEqual("denied", row["service_verdict"])

    def test_delegated_route_is_denied_at_target(self):
        row = self.rows[6]
        self.assertEqual("delegated", row["route"])
        self.assertEqual("denied", row["service_verdict"])
        self.assertEqual("PASS", row["verdict"])

    def test_alternate_route_is_denied_at_target(self):
        row = self.rows[7]
        self.assertEqual("alternate", row["route"])
        self.assertEqual("denied", row["service_verdict"])
        self.assertEqual("PASS", row["verdict"])

    def test_lost_ack_is_reconciled_without_duplicate(self):
        row = self.rows[8]
        self.assertEqual("acknowledgement_lost", row["service_verdict"])
        self.assertEqual("committed", row["operation_readback"]["status"])
        self.assertEqual(1, row["actual_receipt_count"])
        self.assertEqual("PASS", row["verdict"])

    def test_bad_effect_mutant_makes_oracle_fail(self):
        row = self.rows[9]
        self.assertTrue(row["production_changed"])
        self.assertTrue(row["vacuous_text_only_green"])
        self.assertEqual("FAIL", row["verdict"])

    def test_hidden_receipt_still_caught_by_state(self):
        row = one("hidden_receipt_mutant", "crash", "direct",
                  mutant_auth=True, hide_receipts=True)
        self.assertEqual([], row["visible_receipts"])
        self.assertTrue(row["production_changed"])
        self.assertEqual("FAIL", row["verdict"])


if __name__ == "__main__":
    unittest.main()
