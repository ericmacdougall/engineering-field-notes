"""Outcome and negative-control tests for the synthetic Week 12 fixture."""

import copy
import unittest
from datetime import datetime, timezone

from packet_gate import (SourceRecord, dispatch_cutover, fixture, make_packet,
                         verify_packet)

NOW = datetime(2026, 12, 11, tzinfo=timezone.utc)
EXPIRY = "2030-01-01T00:00:00Z"
CASE = "migration-214"
COHORT = "cohort-7"


class PacketGateTests(unittest.TestCase):
    def setUp(self):
        self.store = fixture()
        self.record = self.store.current(CASE, COHORT)
        assert self.record is not None
        self.packet = make_packet(self.record, expires_at=EXPIRY)

    def test_open_exception_is_a_hold(self):
        self.assertEqual(verify_packet(self.packet, self.store, NOW), "HOLD")

    def test_forged_digest_is_unknown(self):
        packet = copy.deepcopy(self.packet)
        packet["source_digest"] = "0" * 64
        self.assertEqual(verify_packet(packet, self.store, NOW), "UNKNOWN")

    def test_wrong_task_is_unknown(self):
        packet = copy.deepcopy(self.packet)
        packet["task_id"] = "cutover-another-case"
        self.assertEqual(verify_packet(packet, self.store, NOW), "UNKNOWN")

    def test_future_observation_is_unknown(self):
        packet = copy.deepcopy(self.packet)
        packet["observed_at"] = "2026-12-12T00:00:00Z"
        self.assertEqual(verify_packet(packet, self.store, NOW), "UNKNOWN")

    def test_wrong_cohort_is_unknown(self):
        packet = copy.deepcopy(self.packet)
        packet["cohort_id"] = "cohort-6"
        self.assertEqual(verify_packet(packet, self.store, NOW), "UNKNOWN")

    def test_stale_memory_version_is_unknown(self):
        self.store.replace(SourceRecord(CASE, COHORT, 13, "reconciled", "data-oncall"))
        self.assertEqual(verify_packet(self.packet, self.store, NOW), "UNKNOWN")

    def test_expired_packet_is_unknown(self):
        packet = make_packet(self.record, expires_at="2026-12-10T00:00:00Z")
        self.assertEqual(verify_packet(packet, self.store, NOW), "UNKNOWN")

    def test_missing_source_is_unknown(self):
        packet = copy.deepcopy(self.packet)
        packet["case_id"] = "migration-unknown"
        self.assertEqual(verify_packet(packet, self.store, NOW), "UNKNOWN")

    def test_suppressed_steward_still_cannot_cutover(self):
        events = []
        # No packet is delivered: the final service gate still checks the store.
        self.assertEqual(dispatch_cutover(self.store, CASE, events), "HOLD")
        self.assertEqual(events, [])

    def test_two_reconciled_cohorts_can_cutover_once_in_fixture(self):
        self.store.replace(SourceRecord(CASE, COHORT, 13, "reconciled", "data-oncall"))
        events = []
        self.assertEqual(dispatch_cutover(self.store, CASE, events), "ELIGIBLE")
        self.assertEqual(events, [f"cutover:{CASE}"])

    def test_missing_required_cohort_is_unknown_and_has_no_effect(self):
        self.store._records.pop((CASE, COHORT))
        events = []
        self.assertEqual(dispatch_cutover(self.store, CASE, events), "UNKNOWN")
        self.assertEqual(events, [])


if __name__ == "__main__":
    unittest.main()
