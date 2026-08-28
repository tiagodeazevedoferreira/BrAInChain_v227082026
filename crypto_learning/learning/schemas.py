from dataclasses import dataclass


@dataclass(frozen=True)
class OutcomeRecord:
    token_id: str
    observed_at: str
    model_version: str
    feature_version: str
    entry_score: float
    entry_price: float
    peak_price: float
    exit_price: float
    return_pct: float
    drawdown_pct: float
    peak_capture_pct: float
    exit_reason: str
    market_regime: str


@dataclass(frozen=True)
class EvaluationResult:
    model_version: str
    sample_count: int
    precision: float
    recall: float
    balanced_accuracy: float
    mean_return_pct: float
    max_drawdown_pct: float
    approved: bool
    reasons: tuple[str, ...]
