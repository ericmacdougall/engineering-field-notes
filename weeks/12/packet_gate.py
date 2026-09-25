"""Synthetic, side-effect-free context-packet and cutover gate example.

This is an editorial fixture, not a production authorization system. No model,
retriever, external deployment API, credential or customer data is used.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal


Decision = Literal["HOLD", "ELIGIBLE", "UNKNOWN"]


@dataclass(frozen=True)
class SourceRecord:
    case_id: str
    cohort_id: str
    version: int
    state: Literal["open", "reconciled"]
    owner: str

    def digest(self) -> str:
        payload = json.dumps(self.__dict__, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class ProtectedStore:
    """Pretends to be the host-owned authoritative record store."""

    def __init__(self, records: list[SourceRecord], required: dict[str, set[str]]):
        self._records = {(r.case_id, r.cohort_id): r for r in records}
        self._required = required

    def current(self, case_id: str, cohort_id: str) -> SourceRecord | None:
        return self._records.get((case_id, cohort_id))

    def required_cohorts(self, case_id: str) -> set[str] | None:
        return self._required.get(case_id)

    def replace(self, record: SourceRecord) -> None:
        self._records[(record.case_id, record.cohort_id)] = record


def make_packet(record: SourceRecord, *, expires_at: str,
                observed_at: str = "2026-12-11T00:00:00Z") -> dict:
    """Make an illustrative steward claim; the receiver must still verify it."""
    return {
        "case_id": record.case_id,
        "task_id": f"cutover-{record.case_id}",
        "cohort_id": record.cohort_id,
        "claim": "hold_cutover" if record.state == "open" else "cohort_reconciled",
        "source_uri": f"protected://reconciliation/{record.case_id}/{record.cohort_id}",
        "source_digest": f"sha256:{record.digest()}",
        "effective_version": record.version,
        "observed_at": observed_at,
        "expires_at": expires_at,
        "owner": record.owner,
        "expected_readback": "no cutover event" if record.state == "open" else "eligible cohort",
    }


def verify_packet(packet: dict, store: ProtectedStore, now: datetime) -> Decision:
    """Resolve the cited current source instead of trusting fluent packet text."""
    try:
        case_id = packet["case_id"]
        task_id = packet["task_id"]
        cohort_id = packet["cohort_id"]
        version = packet["effective_version"]
        digest = packet["source_digest"]
        uri = packet["source_uri"]
        claim = packet["claim"]
        owner = packet["owner"]
        expected_readback = packet["expected_readback"]
        observed = datetime.fromisoformat(packet["observed_at"].replace("Z", "+00:00"))
        expiry = datetime.fromisoformat(packet["expires_at"].replace("Z", "+00:00"))
    except (KeyError, TypeError, ValueError, AttributeError):
        return "UNKNOWN"
    if observed.tzinfo is None or expiry.tzinfo is None or observed > now or now >= expiry:
        return "UNKNOWN"
    if not all(isinstance(v, str) and v for v in
               (case_id, task_id, cohort_id, digest, uri, claim, owner, expected_readback)):
        return "UNKNOWN"
    if not isinstance(version, int) or isinstance(version, bool):
        return "UNKNOWN"
    if uri != f"protected://reconciliation/{case_id}/{cohort_id}":
        return "UNKNOWN"
    if task_id != f"cutover-{case_id}":
        return "UNKNOWN"
    current = store.current(case_id, cohort_id)
    if current is None or current.version != version or f"sha256:{current.digest()}" != digest:
        return "UNKNOWN"
    if current.owner != owner:
        return "UNKNOWN"
    expected = "hold_cutover" if current.state == "open" else "cohort_reconciled"
    if claim != expected:
        return "UNKNOWN"
    expected_result = "no cutover event" if current.state == "open" else "eligible cohort"
    if expected_readback != expected_result:
        return "UNKNOWN"
    return "HOLD" if current.state == "open" else "ELIGIBLE"


def dispatch_cutover(store: ProtectedStore, case_id: str, events: list[str]) -> Decision:
    """Final host-owned service gate; the steward packet is not a permit."""
    cohorts = store.required_cohorts(case_id)
    if not cohorts:
        return "UNKNOWN"
    if os.environ.get("PACKET_GATE_TEST_MUTANT") == "1":
        # Deliberate negative control. Never use this mode outside disposable tests.
        events.append(f"cutover:{case_id}")
        return "ELIGIBLE"
    records = [store.current(case_id, cohort) for cohort in cohorts]
    if any(record is None for record in records):
        return "UNKNOWN"
    if any(record.state != "reconciled" for record in records):
        return "HOLD"
    events.append(f"cutover:{case_id}")
    return "ELIGIBLE"


def fixture() -> ProtectedStore:
    return ProtectedStore(
        [
            SourceRecord("migration-214", "cohort-6", 8, "reconciled", "data-oncall"),
            SourceRecord("migration-214", "cohort-7", 12, "open", "data-oncall"),
        ],
        {"migration-214": {"cohort-6", "cohort-7"}},
    )


def demo() -> None:
    store = fixture()
    current = store.current("migration-214", "cohort-7")
    assert current is not None
    packet = make_packet(current, expires_at="2030-01-01T00:00:00Z")
    now = datetime(2026, 12, 11, tzinfo=timezone.utc)
    events: list[str] = []
    print(json.dumps({
        "packet_verdict": verify_packet(packet, store, now),
        "service_verdict": dispatch_cutover(store, "migration-214", events),
        "target_events": events,
        "scope": "synthetic fixture only",
    }, indent=2))


if __name__ == "__main__":
    demo()
