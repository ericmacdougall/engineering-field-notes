"""Ten synthetic route/denial/effect experiments; no named host is exercised."""
from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path

from fixture import target
from policy import decision

ROOT = Path(__file__).resolve().parent


def get(url: str):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        return json.load(exc)


def send(base: str, op_id: str, tenant: str, token: str = "fixture-stage-token",
         drop_ack: bool = False):
    body = json.dumps({"op_id": op_id, "tenant": tenant, "value": op_id,
                       "drop_ack": drop_ack}).encode()
    request = urllib.request.Request(base + "/mutate", data=body,
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + token}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        return json.load(exc)
    except (ConnectionError, OSError) as exc:
        return {"status": "acknowledgement_lost", "exception": type(exc).__name__}


def fake_hook(principal: str, tenant: str, mode: str) -> str:
    """A deliberately simple simulator, never a claim about a vendor host."""
    if mode in {"crash", "malformed", "timeout", "missing"}:
        return "error:" + mode
    result = decision({"call_id": "synthetic-host-call", "principal": principal, "tenant": tenant})
    return "allow" if result["allowed"] else "deny"


def one(name: str, hook_mode: str, route: str, tenant: str = "production",
        authorized: bool = False, drop_ack: bool = False, mutant_auth: bool | None = None,
        hide_receipts: bool = False):
    with target(mutant_auth=mutant_auth, hide_receipts=hide_receipts) as (base, state):
        before = get(base + "/state")
        hook = fake_hook("staging", tenant, hook_mode)
        # Simulate a permissive host failure route. A deliberate deny stops
        # dispatch; every error or alternate path reaches the service.
        dispatched = hook != "deny" or route in {"delegated", "alternate", "missing_worker"}
        if dispatched:
            service = send(base, name, tenant, drop_ack=drop_ack)
        else:
            service = {"status": "not_dispatched"}
        after = get(base + "/state")
        receipts = get(base + "/receipts")
        operation = get(base + "/operations/" + name) if dispatched else None
        actual_receipts = list(state.receipts)  # independent fixture control
        prod_effect = before["tenants"]["production"] != after["tenants"]["production"]
        reported_tool_text = "blocked" if hook == "deny" else service["status"]
        if authorized:
            passed = (after["tenants"]["staging"] == name and
                      len(actual_receipts) == 1 and operation["status"] == "committed")
        else:
            passed = (not prod_effect and not any(r["tenant"] == "production" for r in actual_receipts))
        record = {"probe": name, "kind": "synthetic_fixture_only", "host": "synthetic-host-simulator-v1",
                  "route": route, "call_id": name, "hook_decision": hook,
                  "reported_tool_text": reported_tool_text,
                  "vacuous_text_only_green": "blocked" in reported_tool_text,
                  "service_verdict": service["status"], "operation_readback": operation,
                  "visible_receipts": receipts, "actual_receipt_count": len(actual_receipts),
                  "target_sha_before": before["sha256"], "target_sha_after": after["sha256"],
                  "production_changed": prod_effect, "verdict": "PASS" if passed else "FAIL"}
        return record


def suite():
    return [
        one("01_allowed_staging", "normal", "direct", tenant="staging", authorized=True),
        one("02_direct_forbidden", "normal", "direct"),
        one("03_hook_crash", "crash", "direct"),
        one("04_malformed_hook", "malformed", "direct"),
        one("05_hook_timeout", "timeout", "direct"),
        one("06_missing_worker_hook", "missing", "missing_worker"),
        one("07_delegated_route", "normal", "delegated"),
        one("08_alternate_tool", "normal", "alternate"),
        one("09_lost_ack_after_commit", "normal", "direct", tenant="staging",
            authorized=True, drop_ack=True),
        one("10_bad_effect_mutant", "normal", "delegated", mutant_auth=True),
    ]


def main():
    records = suite()
    payload = {"fixture": "loopback_http_synthetic", "real_host_probes": 0,
               "real_customer_effects": 0, "records": records,
               "expected_negative_control": "10_bad_effect_mutant must FAIL while a text-only check would pass"}
    (ROOT / "local-evidence.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for row in records:
        print(f"{row['probe']}: {row['verdict']} hook={row['hook_decision']} service={row['service_verdict']}")
    good = all(r["verdict"] == "PASS" for r in records[:9])
    bad_caught = records[9]["verdict"] == "FAIL"
    if not (good and bad_caught):
        raise SystemExit("Synthetic fixture did not meet protected and negative-control gates")


if __name__ == "__main__":
    main()
