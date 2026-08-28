from __future__ import annotations
from dataclasses import dataclass, asdict
from .metrics import classification_metrics


@dataclass(frozen=True)
class EvaluationSummary:
    model_version: str
    dataset_version: str
    sample_count: int
    oos: bool
    metrics: dict


def evaluate_binary(model_version: str, dataset_version: str, tp: int, fp: int, fn: int, tn: int, mean_return_pct: float, max_drawdown_pct: float, peak_capture_pct: float, oos: bool = True) -> EvaluationSummary:
    metrics = classification_metrics(tp, fp, fn, tn)
    metrics.update({
        "mean_return_pct": mean_return_pct,
        "max_drawdown_pct": max_drawdown_pct,
        "peak_capture_pct": peak_capture_pct,
    })
    return EvaluationSummary(model_version, dataset_version, sum([tp, fp, fn, tn]), oos, metrics)


def walk_forward_windows(records: list[dict], train_size: int, test_size: int, step: int | None = None):
    if train_size <= 0 or test_size <= 0:
        raise ValueError("window sizes must be positive")
    step = step or test_size
    ordered = sorted(records, key=lambda r: str(r["observed_at"]))
    for start in range(0, max(0, len(ordered) - train_size - test_size + 1), step):
        yield ordered[start:start + train_size], ordered[start + train_size:start + train_size + test_size]
