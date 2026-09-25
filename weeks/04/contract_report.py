"""Reconcile a synthetic allocation ledger to accepted completed results.

No cluster, provider or billing API is called. The report deliberately does
not infer a first-start SLA from additive queue minutes across retries.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


FIELDS = {
    "provider", "request_id", "attempt_id", "request_state", "gpu_count",
    "gpu_hour_usd", "billed_gpu_minutes", "queue_minutes",
    "requested_topology", "actual_topology", "accepted",
}
STATES = {"accepted", "failed", "open"}
CENT = Decimal("0.01")


def _number(value: str, name: str, identity: tuple[str, str]) -> Decimal:
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid {name} for {identity}") from exc
    if not number.is_finite() or number < 0:
        raise ValueError(f"Invalid {name} for {identity}")
    return number


def parse(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not FIELDS.issubset(reader.fieldnames):
            raise ValueError(f"CSV must include: {', '.join(sorted(FIELDS))}")
        raw_rows = list(reader)
    if not raw_rows:
        raise ValueError("No allocation attempts")

    seen_attempts: set[tuple[str, str]] = set()
    rows: list[dict] = []
    for raw in raw_rows:
        provider, request_id, attempt_id = (
            (raw.get(name) or "").strip()
            for name in ("provider", "request_id", "attempt_id")
        )
        if not provider or not request_id or not attempt_id:
            raise ValueError("Provider, request and attempt IDs are required")
        identity = (provider, attempt_id)
        if identity in seen_attempts:
            raise ValueError(f"Duplicate provider/attempt ID: {identity}")
        seen_attempts.add(identity)

        state = (raw.get("request_state") or "").strip().lower()
        if state not in STATES:
            raise ValueError(f"Invalid request_state for {identity}")
        try:
            gpu_count = int(raw["gpu_count"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid gpu_count for {identity}") from exc
        if gpu_count <= 0:
            raise ValueError(f"Invalid gpu_count for {identity}")
        accepted_text = (raw.get("accepted") or "").strip().lower()
        if accepted_text not in {"true", "false"}:
            raise ValueError(f"accepted must be true or false for {identity}")
        requested = (raw.get("requested_topology") or "").strip()
        actual = (raw.get("actual_topology") or "").strip()
        if not requested or not actual:
            raise ValueError(f"Missing topology class for {identity}")
        rows.append({
            "provider": provider,
            "request_id": request_id,
            "attempt_id": attempt_id,
            "request_state": state,
            "gpu_count": gpu_count,
            "gpu_hour_usd": _number(raw["gpu_hour_usd"], "gpu_hour_usd", identity),
            "billed_gpu_minutes": _number(raw["billed_gpu_minutes"], "billed_gpu_minutes", identity),
            "queue_minutes": _number(raw["queue_minutes"], "queue_minutes", identity),
            "requested_topology": requested,
            "actual_topology": actual,
            "accepted": accepted_text == "true",
        })
    return rows


def percentile(values: list[Decimal], fraction: Decimal) -> Decimal | None:
    if not values:
        return None
    ordered = sorted(values)
    index = Decimal(len(ordered) - 1) * fraction
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (index - lower)


def report(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("No allocation attempts")
    groups: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        groups[row["provider"]][row["request_id"]].append(row)

    output: dict[str, dict] = {}
    for provider, requests in sorted(groups.items()):
        billed = Decimal("0")
        accepted_count = failed_count = open_count = mismatches = attempts_count = 0
        queue_totals: list[Decimal] = []
        for request_id, attempts in requests.items():
            states = {attempt["request_state"] for attempt in attempts}
            topologies = {attempt["requested_topology"] for attempt in attempts}
            if len(states) != 1 or len(topologies) != 1:
                raise ValueError(f"Conflicting request contract for {provider}/{request_id}")
            state = next(iter(states))
            accepted = sum(attempt["accepted"] for attempt in attempts)
            if accepted > 1:
                raise ValueError(f"More than one accepted result for {provider}/{request_id}")
            if accepted != (state == "accepted"):
                raise ValueError(f"Accepted flag conflicts with request_state for {provider}/{request_id}")
            accepted_count += state == "accepted"
            failed_count += state == "failed"
            open_count += state == "open"
            attempts_count += len(attempts)
            queue_totals.append(sum((a["queue_minutes"] for a in attempts), Decimal("0")))
            for attempt in attempts:
                # billed_gpu_minutes already sums the billable minutes across GPUs.
                billed += attempt["gpu_hour_usd"] * attempt["billed_gpu_minutes"] / 60
                mismatches += attempt["actual_topology"] != attempt["requested_topology"]

        # A cohort with open requests has an incomplete denominator. Do not
        # publish a comparable completed-run unit cost for it.
        completed_cost = (
            str((billed / accepted_count).quantize(CENT))
            if accepted_count and not open_count else None
        )
        queue_p95 = percentile(queue_totals, Decimal("0.95"))
        output[provider] = {
            "requests": len(requests),
            "attempts": attempts_count,
            "accepted_results": accepted_count,
            "failed_requests": failed_count,
            "open_requests": open_count,
            "observed_billed_usd": str(billed.quantize(CENT)),
            "completed_cohort_cost_per_accepted_usd": completed_cost,
            "p95_sum_of_queue_intervals_minutes": str(queue_p95.quantize(CENT)) if queue_p95 is not None else None,
            "topology_mismatched_attempts": mismatches,
            "first_start_sla_verdict": "not_measured",
        }
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    print(json.dumps(report(parse(args.csv_path)), indent=2))


if __name__ == "__main__":
    main()
