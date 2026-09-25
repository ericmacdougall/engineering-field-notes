"""Owner-labeled expected outcomes and a replay fault probe.

For the runnable illustration this sits beside candidate.py. In deployment,
copy the acceptance fixture and grader outside the worker's writable scope.
"""

from __future__ import annotations

import os
import sqlite3
import unittest

from candidate import audit_count, import_rows, initialize, read_audit_events, read_states


RECORDS = [
    {"record_id": "old-valid", "approved": True, "revoked": False,
     "source_policy": "legacy-certified", "evidence_ref": "synthetic-audit-01"},
    {"record_id": "old-ambiguous", "approved": True, "revoked": False,
     "source_policy": "", "evidence_ref": ""},
    {"record_id": "old-revoked", "approved": True, "revoked": True,
     "source_policy": "legacy-certified", "evidence_ref": "synthetic-revocation-02"},
    {"record_id": "old-pending", "approved": False, "revoked": False,
     "source_policy": "legacy-certified", "evidence_ref": ""},
]

EXPECTED = {
    "old-valid": "LEGACY_APPROVED",
    "old-ambiguous": "QUARANTINED",
    "old-revoked": "REVOKED",
    "old-pending": "PENDING",
}
EXPECTED_AUDIT = sorted(
    (f"migration-v1:{record_id}", record_id, state)
    for record_id, state in EXPECTED.items()
)


class MigrationContract(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        initialize(self.connection)
        self.mutation = os.environ.get("FIELD_NOTES_MUTATION", "")

    def tearDown(self) -> None:
        self.connection.close()

    def test_owner_labeled_historical_states(self) -> None:
        import_rows(self.connection, RECORDS, attempt_id="first", mutation=self.mutation)
        self.assertEqual(read_states(self.connection), EXPECTED)
        self.assertEqual(audit_count(self.connection), len(RECORDS))
        self.assertEqual(read_audit_events(self.connection), EXPECTED_AUDIT)

    def test_lost_checkpoint_replay_does_not_duplicate_audit_effect(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "lost checkpoint"):
            import_rows(self.connection, RECORDS, attempt_id="first",
                        crash_after=2, mutation=self.mutation)
        self.assertEqual(audit_count(self.connection), 2)
        # The caller's checkpoint did not move; it replays the entire input.
        import_rows(self.connection, RECORDS, attempt_id="retry", mutation=self.mutation)
        self.assertEqual(read_states(self.connection), EXPECTED)
        self.assertEqual(audit_count(self.connection), len(RECORDS))
        self.assertEqual(read_audit_events(self.connection), EXPECTED_AUDIT)


if __name__ == "__main__":
    unittest.main()
