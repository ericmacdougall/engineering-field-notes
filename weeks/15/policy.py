"""Host-neutral fixture policy. Real service authorization lives in fixture.py.

Input JSON: {"call_id": "...", "principal": "staging", "tenant": "staging"}.
Missing, malformed or unknown values deny. This module does not parse arbitrary
shell commands or infer identity from an agent's prose.
"""
from __future__ import annotations

import json
import sys


def decision(payload: object) -> dict:
    if not isinstance(payload, dict):
        return {"allowed": False, "reason": "invalid object"}
    for field in ("call_id", "principal", "tenant"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            return {"allowed": False, "reason": f"missing {field}"}
    if payload["principal"] not in {"staging", "production"} or payload["tenant"] not in {"staging", "production"}:
        return {"allowed": False, "reason": "unknown principal or tenant"}
    allowed = payload["principal"] == payload["tenant"]
    return {"allowed": allowed, "reason": "same tenant" if allowed else "cross-tenant mutation",
            "call_id": payload["call_id"]}


def main():
    try:
        raw = sys.stdin.read(4097)
        if len(raw) > 4096:
            raise ValueError("oversize")
        payload = json.loads(raw)
    except (ValueError, json.JSONDecodeError):
        payload = None
    result = decision(payload)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
