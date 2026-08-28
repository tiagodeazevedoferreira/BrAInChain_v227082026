from __future__ import annotations
from dataclasses import dataclass
from .schemas import EvaluationResult


@dataclass(frozen=True)
class PromotionPolicy:
    min_samples: int = 200
    min_balanced_accuracy: float = 0.55
    min_mean_return_pct: float = 0.0
    max_drawdown_pct: float = 50.0


def evaluate_candidate(result: EvaluationResult, policy: PromotionPolicy | None = None) -> EvaluationResult:
    policy = policy or PromotionPolicy()
    reasons: list[str] = []
    if result.sample_count < policy.min_samples:
        reasons.append("insufficient_samples")
    if result.balanced_accuracy < policy.min_balanced_accuracy:
        reasons.append("balanced_accuracy_below_gate")
    if result.mean_return_pct <= policy.min_mean_return_pct:
        reasons.append("mean_return_not_positive")
    if result.max_drawdown_pct > policy.max_drawdown_pct:
        reasons.append("drawdown_above_gate")
    return EvaluationResult(
        result.model_version, result.sample_count, result.precision, result.recall,
        result.balanced_accuracy, result.mean_return_pct, result.max_drawdown_pct,
        not reasons, tuple(reasons),
    )


def promote(champion: EvaluationResult, challenger: EvaluationResult) -> bool:
    """Promotion requires an already-approved challenger and strict improvement."""
    if not challenger.approved:
        return False
    return (
        challenger.balanced_accuracy > champion.balanced_accuracy
        and challenger.mean_return_pct > champion.mean_return_pct
        and challenger.max_drawdown_pct <= champion.max_drawdown_pct
    )
