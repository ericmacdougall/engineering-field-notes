"""Ten synthetic fault probes corresponding to the Week 13 article."""

import unittest

from fixture import EXPECTED, Journal, accepted_case


class RecoveryTests(unittest.TestCase):
    def test_01_reply_lost_before_commit(self):
        case = Journal("case", "op", "owner")
        case.dispatch()
        self.assertEqual("EFFECT_UNKNOWN", case.classify())
        self.assertFalse(case.may_second_move())

    def test_02_reply_lost_after_commit(self):
        case = accepted_case()
        self.assertFalse(case.reply_seen)
        self.assertEqual("ACCEPTED_PENDING", case.classify())
        self.assertFalse(case.may_second_move())

    def test_03_summary_without_operation_id(self):
        case = Journal("case", None, "owner", dispatched=True)
        self.assertEqual("REQUIRES_OWNER", case.classify())

    def test_04_protected_journal_survives_resume(self):
        case = accepted_case()
        self.assertEqual(["dispatch:move-214", "accepted:move-214"], case.events)
        self.assertEqual("ACCEPTED_PENDING", case.classify())

    def test_05_duplicate_operation_id(self):
        case = accepted_case()
        case.accept()
        self.assertEqual(1, len(case.accepted_ids))
        self.assertEqual(1, case.events.count("accepted:move-214"))
        self.assertEqual("ACCEPTED_PENDING", case.classify())

    def test_06_late_child_after_parent(self):
        case = accepted_case()
        case.branches = dict(EXPECTED)
        case.branches["serving"] = "draining"
        self.assertEqual("ACCEPTED_PENDING", case.classify())
        case.deadline_expired = True
        self.assertEqual("DIVERGED", case.classify())

    def test_07_late_success_same_operation(self):
        case = accepted_case()
        case.branches = dict(EXPECTED)
        self.assertEqual("CONVERGED", case.classify())
        self.assertEqual({"move-214"}, case.accepted_ids)

    def test_08_concurrent_version_blocks_compensation(self):
        case = accepted_case()
        case.current_version = 42
        case.branches["route"] = "A"
        self.assertEqual("REQUIRES_OWNER", case.classify())
        self.assertFalse(case.may_compensate())

    def test_09_unbound_child_message(self):
        case = accepted_case()
        case.branches = dict(EXPECTED)
        case.child_correlation_ok = False
        self.assertEqual("REQUIRES_OWNER", case.classify())

    def test_10_missing_readback(self):
        case = accepted_case()
        case.branches = dict(EXPECTED)
        case.readback_available = False
        self.assertEqual("EFFECT_UNKNOWN", case.classify())


if __name__ == "__main__":
    unittest.main()
