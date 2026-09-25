import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from control_gate import digest_record, evaluate  # noqa: E402


def packet(name="allowed-unobserved"):
    return json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8"))


class ControlGateTests(unittest.TestCase):
    def test_valid_json_can_still_be_forbidden(self):
        self.assertEqual(evaluate(packet("blocked"))["proposal_status"], "AUTHORITY_REJECTED")

    def test_allowed_without_readback_is_unknown(self):
        self.assertEqual(evaluate(packet())["outcome_status"], "UNKNOWN")

    def test_malformed_route_is_rejected(self):
        case = packet()
        case["proposal"]["route"] = "send_everywhere"
        self.assertEqual(evaluate(case)["proposal_status"], "FORMAT_REJECTED")

    def test_unexpected_field_is_rejected(self):
        case = packet()
        case["proposal"]["secret_override"] = True
        self.assertEqual(evaluate(case)["proposal_status"], "FORMAT_REJECTED")

    def test_forged_evidence_digest_is_rejected(self):
        case = packet()
        case["evidence"]["record"]["id"] = "changed"
        self.assertEqual(evaluate(case)["proposal_status"], "EVIDENCE_MISSING")

    def test_valid_digest_with_wrong_evidence_id_is_rejected(self):
        case = packet()
        case["evidence"]["record"]["id"] = "other-record"
        case["evidence"]["sha256"] = digest_record(case["evidence"]["record"])
        self.assertEqual(evaluate(case)["proposal_status"], "EVIDENCE_MISSING")

    def test_stale_policy_version_is_rejected(self):
        case = packet()
        case["proposal"]["policy_version"] = "v1"
        self.assertEqual(evaluate(case)["proposal_status"], "AUTHORITY_REJECTED")

    def test_permit_scope_is_rejected(self):
        case = packet()
        case["permit"]["recipient"] = "different-partner"
        self.assertEqual(evaluate(case)["proposal_status"], "AUTHORITY_REJECTED")

    def test_expired_permit_is_rejected(self):
        case = packet()
        case["permit"]["expires_at"] = "2026-09-24T23:59:59Z"
        self.assertEqual(evaluate(case)["proposal_status"], "AUTHORITY_REJECTED")

    def test_target_readback_must_match_request(self):
        case = packet()
        case["observation"] = {"request_id": "wrong", "recipient": "partner-a", "status": "present"}
        self.assertEqual(evaluate(case)["outcome_status"], "CONFLICT")
        case["observation"]["request_id"] = case["proposal"]["request_id"]
        self.assertEqual(evaluate(case)["outcome_status"], "OBSERVED_SUCCESS")


if __name__ == "__main__":
    unittest.main()
