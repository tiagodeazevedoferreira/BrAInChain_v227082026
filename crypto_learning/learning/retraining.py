from __future__ import annotations
from pathlib import Path
import json


def append_outcome(path: str | Path, outcome: dict) -> Path:
    """Append-only outcome journal. No Firebase historical growth."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(outcome, sort_keys=True, separators=(",", ":")) + "\n")
    return target


def build_training_manifest(outcomes: list[dict], feature_version: str, label_version: str) -> dict:
    return {
        "records": len(outcomes),
        "feature_version": feature_version,
        "label_version": label_version,
        "time_ordered": all(
            str(outcomes[i]["observed_at"]) <= str(outcomes[i + 1]["observed_at"])
            for i in range(len(outcomes) - 1)
        ),
    }
