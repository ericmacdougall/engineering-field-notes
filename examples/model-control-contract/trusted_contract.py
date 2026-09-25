"""Owner-held acceptance and dispatch checks, separate from worker proposals.

Fixtures and policy here are synthetic. A real product needs its policy owner
to replace them with actual authority, cases, and readback.
"""

from __future__ import annotations


CHOICES = {"needs_evidence", "notify_customer", "review_entitlement", "approve_refund"}


class ContractViolation(ValueError):
    pass


def expected_refund_choice(case: dict[str, object]) -> str:
    """Synthetic owner's rule; confidence is intentionally not authorization."""
    if case["settlement"] in {"pending", "unknown"}:
        return "needs_evidence"
    if case["refund_approved"] and case["settlement"] == "settled":
        return "notify_customer"
    return "review_entitlement"


def accept_refund_proposal(case: dict[str, object], proposal: dict[str, object]) -> str:
    choice = proposal.get("choice")
    if choice not in CHOICES:
        raise ContractViolation("proposal is outside the declared choice grammar")
    expected = expected_refund_choice(case)
    if choice != expected:
        raise ContractViolation(f"typed choice {choice!r} conflicts with owner case {expected!r}")
    return choice


def dispatch_route(proposal: dict[str, object], live_registry: dict[str, object]) -> str:
    """Revalidate immediately before dispatch, after the worker selected a route."""
    if proposal.get("registry_version") != live_registry["version"]:
        raise ContractViolation("route was selected against a stale registry")
    if proposal.get("provider") != live_registry["provider"]:
        raise ContractViolation("provider changed before dispatch")
    if proposal.get("tool") not in live_registry["allowed_tools"]:
        raise ContractViolation("tool is no longer authorized")
    return str(proposal["tool"])
