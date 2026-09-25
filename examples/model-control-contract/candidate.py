"""Illustrative worker proposals. No Jev or other model is called here."""

from __future__ import annotations


def propose_refund(case: dict[str, object]) -> dict[str, object]:
    """Return a typed proposal, leaving permission to a separate owner gate."""
    if case["settlement"] in {"pending", "unknown"}:
        choice = "needs_evidence"
    elif case["refund_approved"] and case["settlement"] == "settled":
        choice = "notify_customer"
    else:
        choice = "review_entitlement"
    return {"choice": choice, "confidence": 0.98}


def broken_refund_proposal(case: dict[str, object]) -> dict[str, object]:
    """Deliberate fault: a valid choice that ignores settlement state."""
    return {"choice": "approve_refund", "confidence": 0.99}


def propose_route(snapshot: dict[str, object]) -> dict[str, object]:
    """A host-visible route proposal bound to the registry the worker saw."""
    return {
        "provider": snapshot["provider"],
        "tool": "lookup_settlement",
        "registry_version": snapshot["version"],
    }
