"""Acceptance tests intended for a trusted runner outside an agent-writable worktree."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import pytest

from candidate import FakeProvider, PaymentGateway, connection, initialize, reserve


def test_last_unit_and_repeated_intent(tmp_path):
    path = tmp_path / "store.db"
    initialize(path)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda intent: reserve(path, "last-unit", intent), ("buyer-a", "buyer-b")))
    assert sorted(results) == [False, True]
    with connection(path) as db:
        remaining = db.execute("SELECT available FROM inventory WHERE sku='last-unit'").fetchone()[0]
        intents = [row[0] for row in db.execute("SELECT intent FROM reservations")]
    assert remaining == 0
    assert len(intents) == 1
    assert reserve(path, "last-unit", intents[0])
    with connection(path) as db:
        assert db.execute("SELECT COUNT(*) FROM reservations").fetchone()[0] == 1


def test_lost_ack_reuses_key_and_late_retry_reconciles(tmp_path):
    path = tmp_path / "store.db"
    initialize(path)
    provider = FakeProvider()
    gateway = PaymentGateway(path, provider)
    with pytest.raises(ConnectionError, match="lost acknowledgement"):
        gateway.charge("checkout-7", drop_ack=True)
    first_call_key = provider.calls[0][1]
    gateway.charge("checkout-7")
    assert provider.calls[1][1] == first_call_key
    assert len(provider.captures_for_intent("checkout-7")) == 1
    provider.prune_keys()
    gateway.charge("checkout-7", after_retention=True)
    assert len(provider.captures_for_intent("checkout-7")) == 1
    assert len(provider.calls) == 2
