"""Synthetic computer-use acceptance receipt; no browser or real account access."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def evaluate(contract: dict[str, Any], journey: dict[str, Any],
             authority: dict[str, Any] | None, fresh_session: dict[str, Any] | None,
             effects: dict[str, Any] | None) -> dict[str, Any]:
    failures: list[str] = []
    unknown: list[str] = []

    request = contract.get("request_id")
    tenant = contract.get("tenant")
    account = contract.get("account")
    target_role = contract.get("target_role")
    if not all(isinstance(value, str) and value for value in
               (request, tenant, account, target_role)):
        return {"state": "UNVERIFIED", "failures": [],
                "missing_evidence": ["contract identity or target missing"],
                "limit": "Synthetic receipt only; no live authorization or model test."}

    if journey.get("tenant") != tenant or journey.get("account") != account:
        failures.append("navigator used the wrong tenant or account")
    if journey.get("request_id") != request:
        unknown.append("navigation trace is not bound to this request")
    # A toast is retained for diagnosis, not promoted to acceptance evidence.
    if not journey.get("action_trace_id"):
        unknown.append("navigation trace identity missing")

    if authority is None:
        unknown.append("authoritative readback absent")
    else:
        if authority.get("tenant") != tenant or authority.get("account") != account:
            failures.append("authoritative readback points at a different subject")
        if authority.get("request_id") != request:
            unknown.append("authoritative readback lacks matching request identity")
        if authority.get("policy_status") == "REJECTED":
            failures.append("policy rejected the requested role")
        elif authority.get("policy_status") != "COMMITTED":
            unknown.append("policy commit is not confirmed")
        if authority.get("persisted_role") != target_role:
            if authority.get("policy_status") == "COMMITTED":
                failures.append("persisted role differs from target")
            else:
                unknown.append("target role not yet observed")
        if not authority.get("audit_event_id"):
            unknown.append("independent audit event missing")

    if fresh_session is None:
        unknown.append("fresh-session role check absent")
    else:
        if fresh_session.get("tenant") != tenant or fresh_session.get("account") != account:
            failures.append("fresh session points at a different subject")
        if fresh_session.get("effective_role") != target_role:
            failures.append("fresh session does not have target role")
        if fresh_session.get("unauthorized_action_denied") is not True:
            failures.append("fresh-session negative permission check did not deny")

    if effects is None:
        unknown.append("downstream effect readback absent")
    else:
        count = effects.get("notifications_for_request")
        if not isinstance(count, int) or isinstance(count, bool):
            unknown.append("notification count unavailable")
        elif count != contract.get("expected_notification_count", 1):
            failures.append("notification effect count differs from contract")

    state = "FAIL" if failures else "UNVERIFIED" if unknown else "PASS"
    return {"state": state, "failures": failures, "missing_evidence": unknown,
            "limit": "Synthetic receipt only; no live authorization or model test."}


def main() -> int:
    if len(sys.argv) != 6:
        print("usage: python acceptance_receipt.py contract.json journey.json authority.json fresh-session.json effects.json",
              file=sys.stderr)
        return 2
    values = [json.loads(Path(path).read_text(encoding="utf-8")) for path in sys.argv[1:]]
    receipt = evaluate(*values)
    print(json.dumps(receipt, indent=2))
    return {"PASS": 0, "FAIL": 1, "UNVERIFIED": 3}[receipt["state"]]


if __name__ == "__main__":
    raise SystemExit(main())
