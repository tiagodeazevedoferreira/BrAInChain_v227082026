"""Small, explicit baseline model. Production promotion is intentionally out of scope."""
from __future__ import annotations


def train_baseline(samples: list[dict]) -> dict:
    """Return deterministic dataset statistics when ML dependencies are unavailable."""
    labeled = [s for s in samples if s.get("label") not in (None, "UNKNOWN")]
    counts: dict[str, int] = {}
    for sample in labeled:
        label = str(sample["label"])
        counts[label] = counts.get(label, 0) + 1
    return {
        "model": "baseline_statistics",
        "production_ready": False,
        "sample_count": len(samples),
        "labeled_count": len(labeled),
        "class_counts": counts,
    }
