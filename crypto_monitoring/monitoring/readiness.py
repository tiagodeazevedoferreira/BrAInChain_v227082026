from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Gate:
    key: str
    label: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class ReadinessReport:
    ready: bool
    gates: tuple[Gate, ...]

    def as_dict(self):
        return {"ready": self.ready, "gates": [asdict(g) for g in self.gates]}


def evaluate_readiness(*, data_quality: bool, sufficient_samples: bool, oos_validated: bool,
                       walk_forward_validated: bool, paper_trading_validated: bool,
                       security_validated: bool, failure_tests_validated: bool,
                       secrets_validated: bool, circuit_breakers_validated: bool,
                       venue_validated: bool = False, owner_approved: bool = False) -> ReadinessReport:
    gates = (
        Gate("data_quality", "Data quality", data_quality, "required"),
        Gate("sample_size", "Sufficient sample", sufficient_samples, "required"),
        Gate("oos", "Out-of-sample validation", oos_validated, "required"),
        Gate("walk_forward", "Walk-forward validation", walk_forward_validated, "required"),
        Gate("paper", "Paper trading", paper_trading_validated, "required"),
        Gate("security", "Security validation", security_validated, "required"),
        Gate("failure_tests", "Failure tests", failure_tests_validated, "required"),
        Gate("secrets", "Secrets security", secrets_validated, "required"),
        Gate("circuit_breakers", "Circuit breakers", circuit_breakers_validated, "required"),
        Gate("venue", "Venue adapter", venue_validated, "required before live"),
        Gate("owner", "Owner approval", owner_approved, "explicit approval required"),
    )
    return ReadinessReport(all(g.passed for g in gates), gates)
