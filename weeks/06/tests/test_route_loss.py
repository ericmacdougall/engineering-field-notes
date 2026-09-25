"""Negative controls for the fictional security triage route."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import route_loss  # noqa: E402


class RouteLossTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads((ROOT / "examples.json").read_text(encoding="utf-8"))

    def test_refusal_stays_open_without_fallback_proposal(self) -> None:
        result = route_loss.evaluate(self.fixture)[0]
        self.assertEqual(result["disposition"], "OPEN_UNFINISHED")
        self.assertEqual(result["owner"], "security-review-queue")
        self.assertTrue(result["policy_review_required"])
        self.assertIsNone(result["fallback_proposal"])
        self.assertFalse(result["action_executed"])

    def test_unavailable_route_can_propose_only_reviewed_match(self) -> None:
        public, restricted = route_loss.evaluate(self.fixture)[1:3]
        self.assertEqual(public["fallback_proposal"], "reviewed-secondary-for-public-synthetic")
        self.assertIsNone(restricted["fallback_proposal"])
        self.assertEqual(public["disposition"], "OPEN_UNFINISHED")
        self.assertFalse(public["action_executed"])

    def test_disabling_data_agreement_blocks_proposal(self) -> None:
        registry = [dict(self.fixture["approved_fallback_routes"][0], data_agreement_reviewed=False)]
        result = route_loss.decide(self.fixture["cases"][1], registry)
        self.assertIsNone(result["fallback_proposal"])

    def test_missing_legal_use_review_blocks_proposal(self) -> None:
        registry = [dict(self.fixture["approved_fallback_routes"][0], legal_use_reviewed=False)]
        result = route_loss.decide(self.fixture["cases"][1], registry)
        self.assertIsNone(result["fallback_proposal"])

    def test_missing_evidence_is_uncertain_and_open(self) -> None:
        result = route_loss.evaluate(self.fixture)[3]
        self.assertEqual(result["upstream_result"], "uncertain")
        self.assertEqual(result["disposition"], "OPEN_UNFINISHED")

    def test_unknown_upstream_kind_fails_to_uncertain(self) -> None:
        case = dict(self.fixture["cases"][0], upstream={"kind": "new-provider-code"})
        result = route_loss.decide(case, self.fixture["approved_fallback_routes"])
        self.assertEqual(result["upstream_result"], "uncertain")
        self.assertEqual(result["disposition"], "OPEN_UNFINISHED")

    def test_completed_response_still_needs_owner_review(self) -> None:
        result = route_loss.evaluate(self.fixture)[4]
        self.assertEqual(result["disposition"], "READY_FOR_OWNER_REVIEW")
        self.assertEqual(result["evidence_id"], "synthetic-evidence-001")
        self.assertFalse(result["action_executed"])

    def test_application_authority_blocks_valid_model_response(self) -> None:
        case = dict(self.fixture["cases"][4], actor_allowed_actions=[])
        result = route_loss.decide(case, self.fixture["approved_fallback_routes"])
        self.assertEqual(result["disposition"], "BLOCKED_BY_APPLICATION_AUTHORITY")
        self.assertFalse(result["action_executed"])

    def test_missing_owner_is_an_error(self) -> None:
        case = dict(self.fixture["cases"][0], owner="")
        with self.assertRaisesRegex(ValueError, "missing named owner"):
            route_loss.decide(case, self.fixture["approved_fallback_routes"])

    def test_duplicate_case_id_is_an_error(self) -> None:
        document = dict(self.fixture, cases=self.fixture["cases"] + [self.fixture["cases"][0]])
        with self.assertRaisesRegex(ValueError, "duplicate case id"):
            route_loss.evaluate(document)


if __name__ == "__main__":
    unittest.main()
