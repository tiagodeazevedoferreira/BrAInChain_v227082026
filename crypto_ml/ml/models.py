"""Stable data contracts for ML samples and predictions."""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MLSample:
    token_id: str
    observed_at: str
    features: dict[str, float]
    label: str | None = None
    horizon_hours: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "token_id": self.token_id,
            "observed_at": self.observed_at,
            "features": self.features,
            "label": self.label,
            "horizon_hours": self.horizon_hours,
        }
