"""Bounded local JSONL storage; Firebase is intentionally not used for history."""
from pathlib import Path
import json


class JsonlSnapshotStore:
    def __init__(self, root: str | Path = "data/snapshots") -> None:
        self.root = Path(root)

    def append(self, dataset: str, record: dict) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / f"{dataset}.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n")
        return path
