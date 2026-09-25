"""Offline route-loss fixture: explicit unfinished states, no external effects.

The registry below is a synthetic eligibility screen for a *proposal*. It is
not legal review, provider permission, dispatch authorization or an API client.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class Result(str, Enum):
    COMPLETED = "completed"
    REFUSED = "refused"
    UNAVAILABLE = "unavailable"
    UNCERTAIN = "uncertain"


@dataclass(frozen=True)
class Adapted:
    result: Result
    reason: str
    classification: str | None = None
    evidence_id: str | None = None


def adapt(response: dict[str, Any]) -> Adapted:
    """Unknown and incomplete upstream states never become empty successes."""
    kind = response.get("kind")
    if kind == Result.REFUSED.value:
        return Adapted(Result.REFUSED, "provider declined this route")
    if kind == Result.UNAVAILABLE.value:
        return Adapted(Result.UNAVAILABLE, "route unavailable")
    if kind != Result.COMPLETED.value:
        return Adapted(Result.UNCERTAIN, "unknown or absent upstream result")
    classification = response.get("classification")
    evidence_id = response.get("evidence_id")
    if not isinstance(classification, str) or not classification.strip():
        return Adapted(Result.UNCERTAIN, "completed response missing classification")
    if not isinstance(evidence_id, str) or not evidence_id.strip():
        return Adapted(Result.UNCERTAIN, "completed response missing evidence id")
    return Adapted(
        Result.COMPLETED,
        "model work complete; business review remains",
        classification.strip(),
        evidence_id.strip(),
    )


def eligible_fallback(case: dict[str, Any], registry: list[dict[str, Any]]) -> str | None:
    """Return one candidate name for an outage; do not dispatch it."""
    for route in registry:
        owner = route.get("owner")
        if (
            route.get("approved") is True
            and route.get("active") is True
            and route.get("permitted_use_reviewed") is True
            and route.get("data_agreement_reviewed") is True
            and route.get("legal_use_reviewed") is True
            and isinstance(owner, str) and owner.strip()
            and case.get("task_class") in route.get("task_classes", [])
            and case.get("data_class") in route.get("data_classes", [])
        ):
            name = route.get("name")
            if isinstance(name, str) and name.strip():
                return name.strip()
    return None


def decide(case: dict[str, Any], registry: list[dict[str, Any]]) -> dict[str, Any]:
    """Require a named owner; preserve every non-completion as work to do."""
    owner = case.get("owner")
    case_id = case.get("id")
    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError("missing case id")
    if not isinstance(owner, str) or not owner.strip():
        raise ValueError(f"{case_id}: missing named owner")
    upstream = case.get("upstream")
    if not isinstance(upstream, dict):
        raise ValueError(f"{case_id}: missing upstream response object")
    adapted = adapt(upstream)
    result: dict[str, Any] = {
        "id": case_id,
        "upstream_result": adapted.result.value,
        "owner": owner.strip(),
        "reason": adapted.reason,
        "action_executed": False,
        "fallback_proposal": None,
        "policy_review_required": adapted.result == Result.REFUSED,
    }
    if adapted.result != Result.COMPLETED:
        result["disposition"] = "OPEN_UNFINISHED"
        # An explicit provider refusal may involve policy or terms. It goes
        # to a named policy owner; this toy does not suggest a bypass route.
        if adapted.result == Result.UNAVAILABLE:
            result["fallback_proposal"] = eligible_fallback(case, registry)
        return result

    requested_action = case.get("requested_action")
    allowed_actions = case.get("actor_allowed_actions", [])
    if not isinstance(allowed_actions, list) or requested_action not in allowed_actions:
        result["disposition"] = "BLOCKED_BY_APPLICATION_AUTHORITY"
        return result
    result["disposition"] = "READY_FOR_OWNER_REVIEW"
    result["classification"] = adapted.classification
    result["evidence_id"] = adapted.evidence_id
    return result


def evaluate(document: dict[str, Any]) -> list[dict[str, Any]]:
    cases = document["cases"]
    ids = [case.get("id") for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case id")
    return [decide(case, document["approved_fallback_routes"]) for case in cases]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python route_loss.py examples.json", file=sys.stderr)
        return 2
    document = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(evaluate(document), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
