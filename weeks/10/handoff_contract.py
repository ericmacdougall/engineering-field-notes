"""Pure, synthetic decision-packet audit; no model or target-system access."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


def canonical_digest(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def audit(source: dict[str, Any], packet: dict[str, Any], ack: dict[str, Any],
          today: date) -> dict[str, Any]:
    issues: list[str] = []
    unknown: list[str] = []
    if source.get("owner") in (None, ""):
        unknown.append("source has no named decision owner")
    if packet.get("source_id") != source.get("id") or packet.get("source_version") != source.get("version"):
        issues.append("packet points at a different source or version")
    if packet.get("source_digest") != canonical_digest(source):
        issues.append("packet source digest does not match protected source")
    if packet.get("target_tenant") != source.get("tenant"):
        issues.append("packet targets a different tenant")
    source_clauses = {entry["id"]: entry["text"] for entry in source.get("material_clauses", [])}
    packet_clauses = {entry["id"]: entry["text"] for entry in packet.get("material_clauses", [])}
    if len(source_clauses) != len(source.get("material_clauses", [])):
        issues.append("duplicate clause IDs in source")
    if len(packet_clauses) != len(packet.get("material_clauses", [])):
        issues.append("duplicate clause IDs in packet")
    for clause_id, text in source_clauses.items():
        if clause_id not in packet_clauses:
            unknown.append(f"material clause missing: {clause_id}")
        elif packet_clauses[clause_id] != text:
            issues.append(f"material clause changed: {clause_id}")
    for clause_id in packet_clauses.keys() - source_clauses.keys():
        issues.append(f"unsupported clause inserted: {clause_id}")
    try:
        expiry = date.fromisoformat(source["expires_on"])
    except (KeyError, TypeError, ValueError):
        unknown.append("source expiry is absent or invalid")
    else:
        if today > expiry:
            issues.append("source decision expired")
    if ack.get("packet_id") != packet.get("id"):
        unknown.append("receiver did not acknowledge this packet")
    missing_ack = set(source_clauses) - set(ack.get("acknowledged_clause_ids", []))
    for clause_id in sorted(missing_ack):
        unknown.append(f"receiver did not acknowledge material clause: {clause_id}")
    if not isinstance(ack.get("receiver"), str) or not ack["receiver"].strip():
        unknown.append("receiver identity missing")
    state = "FAIL" if issues else ("UNVERIFIED" if unknown else "PASS")
    return {
        "state": state,
        "blocking_contradictions": issues,
        "missing_evidence": unknown,
        "execution_authorized": False,
        "limit": "Packet fidelity is one input; business authority and target readback are separate.",
    }


def main() -> int:
    if len(sys.argv) not in (4, 5):
        print("usage: python handoff_contract.py source.json packet.json ack.json [as-of-YYYY-MM-DD]",
              file=sys.stderr)
        return 2
    source, packet, ack = (
        json.loads(Path(path).read_text(encoding="utf-8")) for path in sys.argv[1:4]
    )
    try:
        as_of = date.fromisoformat(sys.argv[4]) if len(sys.argv) == 5 else date.today()
    except ValueError:
        print("as-of date must be YYYY-MM-DD", file=sys.stderr)
        return 2
    result = audit(source, packet, ack, as_of)
    print(json.dumps(result, indent=2))
    return {"PASS": 0, "FAIL": 1, "UNVERIFIED": 3}[result["state"]]


if __name__ == "__main__":
    raise SystemExit(main())
