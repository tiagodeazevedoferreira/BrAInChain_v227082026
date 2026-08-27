"""Future-outcome labeling without turning unavailable futures into negatives."""
from __future__ import annotations


def growth_label(return_pct: float | None) -> str:
    if return_pct is None:
        return "UNKNOWN"
    if return_pct >= 1000:
        return "UP_1000P"
    if return_pct >= 500:
        return "UP_500P"
    if return_pct >= 100:
        return "UP_100P"
    if return_pct >= 50:
        return "UP_50P"
    if return_pct >= 25:
        return "UP_25P"
    if return_pct >= 10:
        return "UP_10P"
    if return_pct <= -50:
        return "DOWN_CRASH"
    return "NEUTRAL"
