"""Small illustrative service under test; SQLite and a fake provider are not production integrations."""
from __future__ import annotations

import os
import sqlite3
import uuid
from pathlib import Path


def connection(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(path, timeout=5, isolation_level=None)
    db.execute("PRAGMA busy_timeout = 5000")
    return db


def initialize(path: Path) -> None:
    with connection(path) as db:
        db.executescript("""
            CREATE TABLE inventory (sku TEXT PRIMARY KEY, available INTEGER NOT NULL CHECK (available >= 0));
            CREATE TABLE reservations (intent TEXT PRIMARY KEY, sku TEXT NOT NULL);
            CREATE TABLE payment_keys (intent TEXT PRIMARY KEY, key TEXT NOT NULL UNIQUE);
            INSERT INTO inventory (sku, available) VALUES ('last-unit', 1);
        """)


def reserve(path: Path, sku: str, intent: str) -> bool:
    with connection(path) as db:
        db.execute("BEGIN IMMEDIATE")
        if db.execute("SELECT 1 FROM reservations WHERE intent=?", (intent,)).fetchone():
            db.execute("COMMIT")
            return True
        row = db.execute(
            "UPDATE inventory SET available=available-1 WHERE sku=? AND available>0 RETURNING sku",
            (sku,),
        ).fetchone()
        if row is None:
            db.execute("COMMIT")
            # A deliberate bad confirmation for the independent contract to catch.
            return os.getenv("COMMERCE_MUTANT") == "1"
        db.execute("INSERT INTO reservations (intent, sku) VALUES (?, ?)", (intent, sku))
        db.execute("COMMIT")
        return True


class FakeProvider:
    def __init__(self) -> None:
        self.by_key: dict[str, dict] = {}
        self.ledger: list[dict] = []
        self.calls: list[tuple[str, str]] = []

    def capture(self, intent: str, key: str) -> dict:
        self.calls.append((intent, key))
        if key in self.by_key:
            return self.by_key[key]
        capture = {"id": f"capture-{len(self.ledger)+1}", "intent": intent, "amount": 79}
        self.ledger.append(capture)
        self.by_key[key] = capture
        return capture

    def captures_for_intent(self, intent: str) -> list[dict]:
        return [row for row in self.ledger if row["intent"] == intent]

    def prune_keys(self) -> None:
        self.by_key.clear()


class PaymentGateway:
    def __init__(self, path: Path, provider: FakeProvider) -> None:
        self.path, self.provider = path, provider

    def charge(self, intent: str, *, drop_ack: bool = False, after_retention: bool = False) -> dict:
        with connection(self.path) as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT key FROM payment_keys WHERE intent=?", (intent,)).fetchone()
            if row is None:
                key = uuid.uuid4().hex
                db.execute("INSERT INTO payment_keys (intent, key) VALUES (?, ?)", (intent, key))
            else:
                key = row[0]
            db.execute("COMMIT")
        if after_retention:
            matches = self.provider.captures_for_intent(intent)
            if matches:
                return matches[0]
            raise RuntimeError("Needs explicit recovery policy after provider key retention")
        # Deliberate per-attempt rekeying violates the persisted-intent contract.
        if os.getenv("COMMERCE_MUTANT") == "1":
            key = uuid.uuid4().hex
        capture = self.provider.capture(intent, key)
        if drop_ack:
            raise ConnectionError("simulated lost acknowledgement after capture")
        return capture
