import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import acceptance_receipt


class ReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = [json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))
                       for name in ("contract.json", "journey.json", "authority.json",
                                    "fresh-session.json", "effects.json")]

    def run_case(self, mutate=None):
        values = copy.deepcopy(self.fixture)
        if mutate:
            mutate(values)
        return acceptance_receipt.evaluate(*values)

    def test_all_independent_receipts_agree(self):
        self.assertEqual(self.run_case()["state"], "PASS")

    def test_green_toast_cannot_override_delayed_policy_rejection(self):
        def mutate(v):
            v[2]["policy_status"] = "REJECTED"
            v[2]["persisted_role"] = "viewer"
        self.assertEqual(self.run_case(mutate)["state"], "FAIL")

    def test_green_toast_cannot_override_wrong_persisted_role(self):
        self.assertEqual(self.run_case(lambda v: v[2].update(persisted_role="viewer"))["state"], "FAIL")

    def test_missing_authoritative_readback_is_unverified(self):
        self.assertEqual(self.run_case(lambda v: v.__setitem__(2, None))["state"], "UNVERIFIED")

    def test_wrong_tenant_navigation_fails(self):
        self.assertEqual(self.run_case(lambda v: v[1].update(tenant="other-tenant"))["state"], "FAIL")

    def test_fresh_session_disagrees(self):
        self.assertEqual(self.run_case(lambda v: v[3].update(effective_role="viewer"))["state"], "FAIL")

    def test_duplicate_effect_fails(self):
        self.assertEqual(self.run_case(lambda v: v[4].update(notifications_for_request=2))["state"], "FAIL")

    def test_missing_request_correlation_is_unverified(self):
        self.assertEqual(self.run_case(lambda v: v[2].pop("request_id"))["state"], "UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
