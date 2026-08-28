from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True)
class MetricTarget:
    key: str
    label: str
    current: Optional[float]
    target: Optional[float]
    direction: str
    unit: str = "%"

    def achieved(self) -> Optional[bool]:
        if self.current is None or self.target is None:
            return None
        return self.current >= self.target if self.direction == "higher" else self.current <= self.target

    def as_dict(self):
        d = asdict(self)
        d["achieved"] = self.achieved()
        return d


def classification_metrics(tp: int, fp: int, fn: int, tn: int) -> dict:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    tpr = recall
    tnr = tn / (tn + fp) if tn + fp else 0.0
    balanced_accuracy = (tpr + tnr) / 2
    return {
        "precision": precision * 100,
        "recall": recall * 100,
        "balanced_accuracy": balanced_accuracy * 100,
        "support": tp + fp + fn + tn,
    }


def default_targets() -> list[MetricTarget]:
    return [
        MetricTarget("precision", "Precision", None, 60, "higher"),
        MetricTarget("recall", "Recall", None, 50, "higher"),
        MetricTarget("balanced_accuracy", "Balanced Accuracy", None, 60, "higher"),
        MetricTarget("mean_return_pct", "Mean Return", None, 0, "higher"),
        MetricTarget("max_drawdown_pct", "Max Drawdown", None, 25, "lower"),
        MetricTarget("peak_capture_pct", "Peak Capture", None, 70, "higher"),
        MetricTarget("two_x_detection_pct", "2x Detection", None, 70, "higher"),
        MetricTarget("five_x_detection_pct", "5x Detection", None, 60, "higher"),
        MetricTarget("ten_x_detection_pct", "10x Detection", None, 40, "higher"),
    ]
