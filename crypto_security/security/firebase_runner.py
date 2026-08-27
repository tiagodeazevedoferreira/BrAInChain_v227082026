from __future__ import annotations

import os
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, db

from .engine import SecurityEngine
from .firebase_sink import FirebaseSecuritySink


def _timestamp(pool: dict) -> str:
    return str(pool.get("discovered_at") or "")


def load_pending_pools(limit: int) -> list[dict]:
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(
            credentials.Certificate(os.environ["FIREBASE_SERVICE_ACCOUNT_FILE"]),
            {"databaseURL": os.getenv("FIREBASE_DATABASE_URL", "https://brainchainv227082026-default-rtdb.firebaseio.com")},
        )

    pools = db.reference("discovery/tokens", app=app).get() or {}
    security = db.reference("security/tokens", app=app).get() or {}
    candidates = []
    for key, pool in pools.items():
        if key in security:
            continue
        if not isinstance(pool, dict) or not pool.get("base_token_address"):
            continue
        candidates.append(pool)
    candidates.sort(key=_timestamp, reverse=True)
    return candidates[:limit]


def run() -> None:
    limit = int(os.getenv("SECURITY_MAX_TOKENS", "25"))
    pools = load_pending_pools(limit)
    engine = SecurityEngine()
    analyses = []
    errors = []
    for pool in pools:
        try:
            analyses.append(engine.analyze(pool))
        except Exception as exc:
            errors.append({"token": pool.get("base_token_address"), "error": str(exc)})

    status = FirebaseSecuritySink().write(analyses, errors)
    print(f"SECURITY_INPUT={len(pools)}")
    print(f"SECURITY_ANALYZED={len(analyses)}")
    print(f"SECURITY_DO_NOT_TRADE={status['do_not_trade_count']}")
    print(f"SECURITY_CRITICAL={status['critical_count']}")
    print("SECURITY_PIPELINE=OK")


if __name__ == "__main__":
    run()
