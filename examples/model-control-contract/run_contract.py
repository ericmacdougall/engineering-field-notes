"""Run normal synthetic cases and two deliberately failing counterexamples."""

from __future__ import annotations

from candidate import broken_refund_proposal, propose_refund, propose_route
from trusted_contract import ContractViolation, accept_refund_proposal, dispatch_route


def must_reject(label: str, action) -> None:
    try:
        action()
    except ContractViolation as exc:
        print(f"REJECTED {label}: {exc}")
        return
    raise AssertionError(f"negative control survived: {label}")


def main() -> None:
    cases = (
        ({"refund_approved": True, "settlement": "pending"}, "needs_evidence"),
        ({"refund_approved": True, "settlement": "settled"}, "notify_customer"),
        ({"refund_approved": False, "settlement": "unknown"}, "needs_evidence"),
    )
    for case, expected in cases:
        accepted = accept_refund_proposal(case, propose_refund(case))
        assert accepted == expected
    print("PASS 3 owner-labeled refund cases")

    pending = cases[0][0]
    must_reject("valid type but wrong action", lambda: accept_refund_proposal(
        pending, broken_refund_proposal(pending)
    ))

    snapshot = {"provider": "billing", "version": "v1", "allowed_tools": {"lookup_settlement"}}
    proposal = propose_route(snapshot)
    assert dispatch_route(proposal, snapshot) == "lookup_settlement"
    print("PASS current route dispatch")
    changed = {"provider": "billing", "version": "v2", "allowed_tools": set()}
    must_reject("stale route after permission change", lambda: dispatch_route(proposal, changed))


if __name__ == "__main__":
    main()
