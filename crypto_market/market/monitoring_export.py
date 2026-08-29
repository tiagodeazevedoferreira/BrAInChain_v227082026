"""Export the latest Firebase market state to the static PWA monitoring feed."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, db


def get_app():
    try:
        return firebase_admin.get_app()
    except ValueError:
        credential_file = os.environ.get("FIREBASE_SERVICE_ACCOUNT_FILE")
        if not credential_file:
            raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_FILE is required")
        return firebase_admin.initialize_app(
            credentials.Certificate(credential_file),
            {"databaseURL": os.environ["FIREBASE_DATABASE_URL"]},
        )


def main():
    app = get_app()
    root = db.reference("/", app=app).get() or {}
    market = root.get("market", {}) or {}
    status = market.get("status", {}) or {}
    tokens = market.get("tokens", {}) or {}
    discovery = root.get("discovery", {}) or {}
    discovery_tokens = discovery.get("tokens", {}) or {}

    last_run = status.get("last_run_at")
    now = datetime.now(timezone.utc)
    age_hours = None
    if last_run:
        try:
            age_hours = max(0, (now - datetime.fromisoformat(last_run.replace("Z", "+00:00"))).total_seconds() / 3600)
        except ValueError:
            pass

    payload = {
        "generated_at": now.isoformat(),
        "collection": {
            "pipeline_status": "HEALTHY" if last_run and age_hours is not None and age_hours <= 6 and status.get("error_count", 0) == 0 else "UNKNOWN",
            "firebase_status": "CONNECTED",
            "observations": len(tokens),
            "valid_observations": len(tokens),
            "rejected_observations": status.get("error_count", 0),
            "tokens_discovered": len(discovery_tokens),
            "growth_24h": "—",
            "last_collection_at": last_run,
            "age_hours": round(age_hours, 2) if age_hours is not None else None,
            "stale": age_hours is None or age_hours > 6,
        },
        "metrics": {},
        "readiness": {"gates": []},
        "source": {
            "market_analysis_count": status.get("analysis_count", 0),
            "market_error_count": status.get("error_count", 0),
            "storage_policy": status.get("storage_policy", "latest_state_only"),
        },
    }

    output = Path(__file__).resolve().parents[2] / "ML_MONITORING" / "data" / "ml-monitoring.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["collection"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
