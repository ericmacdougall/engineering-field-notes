import json
import unittest

from claude_pretool_fixture_example import respond
from policy import decision


class PolicyTests(unittest.TestCase):
    def test_only_same_tenant_is_allowed(self):
        self.assertTrue(decision({"call_id": "a", "principal": "staging", "tenant": "staging"})["allowed"])
        self.assertFalse(decision({"call_id": "b", "principal": "staging", "tenant": "production"})["allowed"])

    def test_missing_and_unknown_fields_deny(self):
        for payload in (None, {}, {"principal": "staging", "tenant": "production"},
                        {"call_id": "x", "principal": "anything", "tenant": "production"}):
            with self.subTest(payload=payload):
                self.assertFalse(decision(payload)["allowed"])

    def test_unmatched_event_denies_in_example(self):
        event = {"hook_event_name": "PostToolUse", "tool_name": "mcp__fixture__mutate",
                 "tool_input": {"call_id": "x", "principal": "staging", "tenant": "staging"}}
        self.assertEqual("deny", respond(json.dumps(event))["hookSpecificOutput"]["permissionDecision"])

    def test_fixture_event_denies_cross_tenant(self):
        event = {"hook_event_name": "PreToolUse", "tool_name": "mcp__fixture__mutate",
                 "tool_input": {"call_id": "x", "principal": "staging", "tenant": "production"}}
        self.assertEqual("deny", respond(json.dumps(event))["hookSpecificOutput"]["permissionDecision"])


if __name__ == "__main__":
    unittest.main()
