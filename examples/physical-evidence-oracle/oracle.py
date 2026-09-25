"""Synthetic, read-only acceptance oracle; never connects to OT equipment."""

from dataclasses import dataclass
from enum import Enum


class Verdict(str, Enum):
    PROBE_PASS = "synthetic probe passed; not plant acceptance"
    CANDIDATE_FAIL = "candidate behavior failed synthetic requirement"
    EVIDENCE_GAP = "evidence incomplete; no acceptance claim"


@dataclass(frozen=True)
class Contract:
    requirement_id: str
    max_sensor_age_ms: int
    stop_observation_ms: int
    max_measured_speed_mps: float
    target_project_hash: str
    reset_requires_operator: bool


@dataclass(frozen=True)
class SyntheticTrace:
    requirement_id: str
    sensor_age_ms: int
    jam_asserted: bool
    motor_command_on: bool
    measured_speed_mps: float | None
    elapsed_since_stop_ms: int
    operator_reset_seen: bool
    automatic_restart: bool
    model_includes_sensor_fault: bool
    project_hash: str
    rollback_recorded: bool


def evaluate(contract: Contract, trace: SyntheticTrace) -> tuple[Verdict, str]:
    """Check one invented trace against owner-supplied requirements.

    Every return is scoped to a synthetic probe, even if it passes.
    A real acceptance needs an approved site procedure and independent physical observation.
    """
    if not contract.requirement_id or not contract.target_project_hash:
        return Verdict.EVIDENCE_GAP, "requirement or target identity not signed"
    if trace.requirement_id != contract.requirement_id:
        return Verdict.EVIDENCE_GAP, "trace is not tied to this requirement"
    if trace.project_hash != contract.target_project_hash:
        return Verdict.EVIDENCE_GAP, "tested project differs from release target"
    if not trace.rollback_recorded:
        return Verdict.EVIDENCE_GAP, "rollback packet missing"
    if not trace.model_includes_sensor_fault:
        return Verdict.EVIDENCE_GAP, "the simulator omits the fault being claimed"
    if trace.sensor_age_ms > contract.max_sensor_age_ms:
        return Verdict.CANDIDATE_FAIL, "stale sensor was used as current evidence"
    if trace.jam_asserted and trace.motor_command_on:
        return Verdict.CANDIDATE_FAIL, "motor remains commanded on during jam"
    if trace.measured_speed_mps is None:
        return Verdict.EVIDENCE_GAP, "command exists but measured motion is absent"
    if (trace.jam_asserted and trace.elapsed_since_stop_ms >= contract.stop_observation_ms
            and trace.measured_speed_mps > contract.max_measured_speed_mps):
        return Verdict.CANDIDATE_FAIL, "measured motion exceeds the required stop observation"
    if contract.reset_requires_operator and trace.automatic_restart and not trace.operator_reset_seen:
        return Verdict.CANDIDATE_FAIL, "automatic restart bypasses required operator reset"
    return Verdict.PROBE_PASS, "this synthetic trace satisfies the stated checks"
