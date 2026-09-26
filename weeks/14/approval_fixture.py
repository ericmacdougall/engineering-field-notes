"""Disposable approval-history oracle for the Week 14 field note.

No customer data, model call, provider API, or SaaS integration is used.
Policies here are owner labels for this fictional exercise only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import os


class State(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Event:
    kind: str
    sequence: int
    policy_version: int | None
    approver: str | None = None
    effective_until: int | None = None


@dataclass(frozen=True)
class Record:
    case_id: str
    events: tuple[Event, ...]
    legacy_approved: bool | None = None
    exception_open: bool = False


@dataclass(frozen=True)
class Verdict:
    state: State
    reason: str
    source_sequence: int | None


def naive_migration(record: Record) -> Verdict:
    """Deliberately defective shortcut: a plausible legacy-flag migration."""
    if record.legacy_approved:
        return Verdict(State.ACTIVE, "legacy flag", None)
    return Verdict(State.INACTIVE, "legacy flag", None)


def protected_decision(record: Record, *, now: int = 100) -> Verdict:
    """Owner-labeled synthetic decision, fail closed on missing provenance."""
    if not record.case_id or record.exception_open:
        return Verdict(State.UNKNOWN, "case or exception needs owner", None)
    if not record.events:
        return Verdict(State.UNKNOWN, "no event provenance", None)
    sequences = [event.sequence for event in record.events]
    if len(sequences) != len(set(sequences)) or sequences != sorted(sequences):
        return Verdict(State.UNKNOWN, "event order is not trustworthy", None)
    latest = record.events[-1]
    if latest.policy_version is None:
        return Verdict(State.UNKNOWN, "policy version missing", latest.sequence)
    if latest.kind == "REVOKED":
        # This mutation is used solely to prove the protected acceptance test
        # detects a false grant. Keep it out of any real release path.
        if os.environ.get("W14_TEST_MUTANT") == "1":
            return Verdict(State.ACTIVE, "MUTANT incorrect grant", latest.sequence)
        return Verdict(State.INACTIVE, "later revocation", latest.sequence)
    if latest.kind == "APPROVED" and latest.approver:
        if latest.effective_until is not None and latest.effective_until < now:
            return Verdict(State.INACTIVE, "approval expired", latest.sequence)
        return Verdict(State.ACTIVE, "current sourced approval", latest.sequence)
    return Verdict(State.UNKNOWN, "unrecognized or unsigned event", latest.sequence)


def resume_from_handoff(record: Record, summary: str, recorded_sequence: int | None) -> Verdict:
    """Handoff prose is a hint; current protected history chooses the state."""
    del summary
    current = protected_decision(record)
    if recorded_sequence is not None and current.source_sequence != recorded_sequence:
        return Verdict(State.UNKNOWN, "handoff stale; current source changed", current.source_sequence)
    return current
