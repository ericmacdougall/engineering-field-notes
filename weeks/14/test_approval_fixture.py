"""Owner-labeled acceptance cases and one deliberate broken-code control."""

import unittest

from approval_fixture import Event, Record, State, naive_migration, protected_decision, resume_from_handoff


class Acceptance(unittest.TestCase):
    def test_valid_historical_approval(self):
        record = Record("A", (Event("APPROVED", 1, 3, "owner"),), True)
        self.assertEqual(protected_decision(record).state, State.ACTIVE)

    def test_later_revocation_must_override_legacy_true(self):
        record = Record("B", (Event("APPROVED", 1, 3, "owner"), Event("REVOKED", 2, 3)), True)
        self.assertEqual(naive_migration(record).state, State.ACTIVE)
        self.assertEqual(protected_decision(record).state, State.INACTIVE)

    def test_ambiguous_legacy_boolean_is_unknown(self):
        record = Record("C", (), True)
        self.assertEqual(protected_decision(record).state, State.UNKNOWN)

    def test_missing_policy_version_is_unknown(self):
        record = Record("D", (Event("APPROVED", 1, None, "owner"),), True)
        self.assertEqual(protected_decision(record).state, State.UNKNOWN)

    def test_missing_approver_is_unknown(self):
        record = Record("E", (Event("APPROVED", 1, 3),), True)
        self.assertEqual(protected_decision(record).state, State.UNKNOWN)

    def test_exception_requires_owner(self):
        record = Record("F", (Event("APPROVED", 1, 3, "owner"),), True, True)
        self.assertEqual(protected_decision(record).state, State.UNKNOWN)

    def test_temporary_mode_requires_expiry_read(self):
        record = Record("G", (Event("APPROVED", 1, 4, "owner", effective_until=50),), True)
        self.assertEqual(protected_decision(record, now=100).state, State.INACTIVE)

    def test_stale_handoff_is_unknown_even_if_summary_says_approved(self):
        record = Record("H", (Event("APPROVED", 1, 3, "owner"), Event("REVOKED", 2, 4)), True)
        self.assertEqual(resume_from_handoff(record, "Customer approved", 1).state, State.UNKNOWN)

    def test_current_handoff_still_reads_source(self):
        record = Record("I", (Event("APPROVED", 1, 3, "owner"),), True)
        self.assertEqual(resume_from_handoff(record, "Customer denied", 1).state, State.ACTIVE)

    def test_order_conflict_is_unknown(self):
        record = Record("J", (Event("APPROVED", 2, 3, "owner"), Event("REVOKED", 1, 3)), True)
        self.assertEqual(protected_decision(record).state, State.UNKNOWN)


if __name__ == "__main__":
    unittest.main()
