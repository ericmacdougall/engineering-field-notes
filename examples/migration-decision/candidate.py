"""A deliberately small, illustrative legacy-approval importer.

All records and policy choices are synthetic. The mutation argument exists
only so the separate contract can prove that two plausible mistakes turn red.
In a real agent workflow the expected outcomes and grader would be outside
the worker's writable checkout.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable


def initialize(connection: sqlite3.Connection) -> None:
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS approval_state (
            record_id TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            source_policy TEXT,
            evidence_ref TEXT
        );
        CREATE TABLE IF NOT EXISTS audit_event (
            event_key TEXT PRIMARY KEY,
            record_id TEXT NOT NULL,
            state TEXT NOT NULL
        );
    """)


def classify(record: dict, mutation: str = "") -> str:
    # This is a synthetic owner-labeled rule, not a universal migration policy.
    if mutation == "accept_every_true":
        return "APPROVED" if record["approved"] else "PENDING"
    if record["revoked"]:
        return "REVOKED"
    if not record["approved"]:
        return "PENDING"
    if record["source_policy"] == "legacy-certified" and record["evidence_ref"]:
        return "LEGACY_APPROVED"
    return "QUARANTINED"


def import_rows(
    connection: sqlite3.Connection,
    records: Iterable[dict],
    *,
    attempt_id: str,
    crash_after: int | None = None,
    mutation: str = "",
) -> None:
    """Commit each effect; a caller may lose its checkpoint and replay all rows."""
    for index, record in enumerate(records, 1):
        state = classify(record, mutation)
        key = f"migration-v1:{record['record_id']}"
        if mutation == "new_key_on_retry":
            key = f"{key}:{attempt_id}"
        with connection:
            connection.execute(
                "INSERT INTO approval_state(record_id,state,source_policy,evidence_ref) "
                "VALUES (?,?,?,?) ON CONFLICT(record_id) DO UPDATE SET "
                "state=excluded.state,source_policy=excluded.source_policy,"
                "evidence_ref=excluded.evidence_ref",
                (record["record_id"], state, record["source_policy"], record["evidence_ref"]),
            )
            connection.execute(
                "INSERT OR IGNORE INTO audit_event(event_key,record_id,state) VALUES (?,?,?)",
                (key, record["record_id"], state),
            )
        if index == crash_after:
            raise RuntimeError("simulated lost checkpoint after committed effect")


def read_states(connection: sqlite3.Connection) -> dict[str, str]:
    return dict(connection.execute("SELECT record_id,state FROM approval_state"))


def audit_count(connection: sqlite3.Connection) -> int:
    return connection.execute("SELECT COUNT(*) FROM audit_event").fetchone()[0]


def read_audit_events(connection: sqlite3.Connection) -> list[tuple[str, str, str]]:
    return list(connection.execute(
        "SELECT event_key,record_id,state FROM audit_event ORDER BY event_key"
    ))
