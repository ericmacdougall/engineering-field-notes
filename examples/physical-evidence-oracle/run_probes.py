"""Ten non-destructive synthetic probes for the Week 05 field note."""

from dataclasses import replace
from oracle import Contract, SyntheticTrace, Verdict, evaluate


contract = Contract(
    requirement_id="FICTIONAL-CONVEYOR-JAM-01", max_sensor_age_ms=200,
    stop_observation_ms=800, max_measured_speed_mps=0.02,
    target_project_hash="fictional-approved-build", reset_requires_operator=True,
)
base = SyntheticTrace(
    requirement_id=contract.requirement_id, sensor_age_ms=40,
    jam_asserted=True, motor_command_on=False, measured_speed_mps=0.0,
    elapsed_since_stop_ms=1000, operator_reset_seen=False,
    automatic_restart=False, model_includes_sensor_fault=True,
    project_hash=contract.target_project_hash, rollback_recorded=True,
)

probes = [
    ("normal synthetic stop", contract, base, Verdict.PROBE_PASS),
    ("requirement ID mismatch", contract, replace(base, requirement_id="other"), Verdict.EVIDENCE_GAP),
    ("target version mismatch", contract, replace(base, project_hash="other"), Verdict.EVIDENCE_GAP),
    ("fault omitted from twin", contract, replace(base, model_includes_sensor_fault=False), Verdict.EVIDENCE_GAP),
    ("stale jam signal", contract, replace(base, sensor_age_ms=350), Verdict.CANDIDATE_FAIL),
    ("jam while output stays on", contract, replace(base, motor_command_on=True), Verdict.CANDIDATE_FAIL),
    ("stop command without motion observation", contract, replace(base, measured_speed_mps=None), Verdict.EVIDENCE_GAP),
    ("motion continues after stop window", contract, replace(base, measured_speed_mps=0.5), Verdict.CANDIDATE_FAIL),
    ("automatic restart without operator reset", contract, replace(base, automatic_restart=True), Verdict.CANDIDATE_FAIL),
    ("rollback packet absent", contract, replace(base, rollback_recorded=False), Verdict.EVIDENCE_GAP),
]

for name, spec, trace, expected in probes:
    verdict, reason = evaluate(spec, trace)
    assert verdict == expected, f"{name}: expected {expected}, got {verdict}: {reason}"
    print(f"PASS {name}: {verdict.value} — {reason}")

print(f"{len(probes)} synthetic probes passed; no plant acceptance or live OT test claimed")
