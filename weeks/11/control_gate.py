"""Evaluate a fictional transfer proposal without performing an action."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROUTES = {"share", "review", "decline"}
REQUIRED_PROPOSAL = {"route", "tenant", "recipient", "operation", "evidence_id", "policy_version", "request_id"}
REQUIRED_POLICY = {"version", "tenant", "external_transfer_allowed", "evidence_id"}
REQUIRED_PERMIT = {"tenant", "recipient", "operation", "policy_version", "expires_at"}


def digest_record(record: dict[str, Any]) -> str:
    raw = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timestamp needs a timezone")
    return parsed.astimezone(timezone.utc)


def result(status: str, reason: str, outcome: str = "SKIPPED") -> dict[str, str]:
    return {"proposal_status": status, "reason": reason, "outcome_status": outcome}


def evaluate(packet: dict[str, Any]) -> dict[str, str]:
    """Return a gate/readback assessment; never dispatch a request."""
    try:
        proposal, policy, evidence, permit = (packet[key] for key in ("proposal", "policy", "evidence", "permit"))
        now = utc(packet["now_utc"])
        if not all(isinstance(part, dict) for part in (proposal, policy, evidence, permit)):
            return result("FORMAT_REJECTED", "A record is not an object")
        if set(proposal) != REQUIRED_PROPOSAL or set(policy) != REQUIRED_POLICY or set(permit) != REQUIRED_PERMIT:
            return result("FORMAT_REJECTED", "Unexpected or missing gate fields")
        if proposal["route"] not in ROUTES or not all(isinstance(proposal[key], str) and proposal[key] for key in REQUIRED_PROPOSAL):
            return result("FORMAT_REJECTED", "Invalid route or proposal field")
        if not isinstance(policy["external_transfer_allowed"], bool):
            return result("FORMAT_REJECTED", "Policy permission is not boolean")
        if not all(isinstance(permit[key], str) and permit[key] for key in REQUIRED_PERMIT):
            return result("FORMAT_REJECTED", "Invalid permit field")
        if set(evidence) != {"record", "sha256"} or not isinstance(evidence["record"], dict):
            return result("FORMAT_REJECTED", "Evidence record has invalid shape")
        if evidence["sha256"] != digest_record(evidence["record"]):
            return result("EVIDENCE_MISSING", "Evidence digest mismatch")
        if evidence["record"].get("id") != proposal["evidence_id"] or policy["evidence_id"] != proposal["evidence_id"]:
            return result("EVIDENCE_MISSING", "Evidence identifier is missing or wrong")
        if evidence["record"].get("policy_version") != policy["version"]:
            return result("EVIDENCE_MISSING", "Evidence does not identify the current policy version")
        if proposal["policy_version"] != policy["version"]:
            return result("AUTHORITY_REJECTED", "Proposal used a stale policy version")
        if proposal["tenant"] != policy["tenant"]:
            return result("AUTHORITY_REJECTED", "Proposal tenant is outside policy scope")
        if proposal["route"] != "share":
            return result("AUTHORITY_REJECTED", "No transfer is proposed")
        if not policy["external_transfer_allowed"]:
            return result("AUTHORITY_REJECTED", "Current policy suspends external transfer")
        if any(permit[key] != proposal[key] for key in ("tenant", "recipient", "operation")):
            return result("AUTHORITY_REJECTED", "Permit does not cover this request")
        if permit["policy_version"] != policy["version"] or utc(permit["expires_at"]) <= now:
            return result("AUTHORITY_REJECTED", "Permit version is stale or permit expired")
        observation = packet.get("observation")
        if observation is None:
            return result("READY_FOR_SEPARATE_DISPATCH", "Synthetic gate passed; no effect is proven", "UNKNOWN")
        if not isinstance(observation, dict) or set(observation) != {"request_id", "recipient", "status"}:
            return result("READY_FOR_SEPARATE_DISPATCH", "Observation is malformed", "UNVERIFIED")
        if (observation["request_id"], observation["recipient"], observation["status"]) == (
            proposal["request_id"], proposal["recipient"], "present"
        ):
            return result("READY_FOR_SEPARATE_DISPATCH", "Synthetic target record matches request", "OBSERVED_SUCCESS")
        return result("READY_FOR_SEPARATE_DISPATCH", "Target record conflicts with request", "CONFLICT")
    except (KeyError, TypeError, ValueError, OverflowError) as error:
        return result("FORMAT_REJECTED", f"Input cannot be assessed: {type(error).__name__}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python control_gate.py packet.json")
    packet = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(evaluate(packet), indent=2))


if __name__ == "__main__":
    main()
