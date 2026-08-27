from __future__ import annotations

import json
import os
from pathlib import Path

from .engine import SecurityEngine
from .firebase_sink import FirebaseSecuritySink


def load_discovery() -> list[dict]:
    raw = os.getenv("DISCOVERY_JSON")
    if raw:
        return json.loads(raw)
    path = Path(os.getenv("DISCOVERY_FILE", "discovery.json"))
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    raise RuntimeError("DISCOVERY_JSON or DISCOVERY_FILE is required")


def main() -> None:
    pools = load_discovery()
    engine = SecurityEngine()
    analyses = []
    errors = []
    for pool in pools:
        try:
            analyses.append(engine.analyze(pool))
        except Exception as exc:
            errors.append({"token": pool.get("base_token_address"), "error": str(exc)})

    sink = FirebaseSecuritySink()
    status = sink.write(analyses, errors)
    print(json.dumps(status, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
