import json
from dataclasses import asdict
from pathlib import Path
from .models import PaperPosition


class PaperLedger:
    """Append-only paper journal outside Firebase."""
    def __init__(self, path: str | Path = "data/paper/trades.jsonl"):
        self.path = Path(path)

    def record(self, position: PaperPosition) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(position), separators=(",", ":"), sort_keys=True) + "\n")

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
