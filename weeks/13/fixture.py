"""Synthetic recovery decision. No remote calls or destructive actions."""

from dataclasses import dataclass, field
import os


EXPECTED = {"placement": "B", "mapping": "B", "route": "B", "serving": "healthy"}


@dataclass
class Journal:
    case_id: str
    operation_id: str | None
    owner: str
    authorized_target: str = "B"
    initial_version: int = 41
    current_version: int = 41
    dispatched: bool = False
    accepted: bool = False
    reply_seen: bool = False
    readback_available: bool = True
    deadline_expired: bool = False
    child_correlation_ok: bool = True
    branches: dict[str, str] = field(default_factory=dict)
    accepted_ids: set[str] = field(default_factory=set)
    events: list[str] = field(default_factory=list)

    def append(self, event: str) -> None:
        self.events.append(event)

    def dispatch(self) -> None:
        if not self.operation_id:
            raise ValueError("stable operation identity required")
        self.dispatched = True
        self.append(f"dispatch:{self.operation_id}")

    def accept(self) -> None:
        if not self.dispatched or not self.operation_id:
            raise ValueError("dispatch first")
        if self.operation_id not in self.accepted_ids:
            self.accepted_ids.add(self.operation_id)
            self.accepted = True
            self.append(f"accepted:{self.operation_id}")

    def classify(self) -> str:
        if not self.operation_id or not self.child_correlation_ok:
            return "REQUIRES_OWNER"
        if not self.dispatched:
            return "NOT_DISPATCHED"
        if not self.readback_available:
            return "EFFECT_UNKNOWN"
        if not self.accepted:
            return "EFFECT_UNKNOWN"
        if self.current_version != self.initial_version and not self.converged():
            return "REQUIRES_OWNER"
        if self.converged():
            return "CONVERGED"
        if self.deadline_expired:
            if any(self.branches.get(name) not in (None, expected) for name, expected in EXPECTED.items()):
                return "DIVERGED"
            return "REQUIRES_OWNER"
        return "ACCEPTED_PENDING"

    def converged(self) -> bool:
        return all(self.branches.get(name) == value for name, value in EXPECTED.items())

    def may_second_move(self) -> bool:
        """An unresolved original effect never authorizes a fresh move."""
        if os.environ.get("W13_TEST_MUTANT") == "1":
            return self.classify() in {"NOT_DISPATCHED", "EFFECT_UNKNOWN"}
        return self.classify() == "NOT_DISPATCHED"

    def may_compensate(self) -> bool:
        """The fixture refuses automatic compensation after version change."""
        return False  # A human/business authorization path is outside this fixture.


def accepted_case() -> Journal:
    case = Journal("gpu-move-214", "move-214", "capacity-oncall")
    case.dispatch()
    case.accept()
    return case
