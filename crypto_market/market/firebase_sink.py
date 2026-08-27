import os
from datetime import datetime, timezone

from .models import IntelligenceAnalysis


class FirebaseMarketSink:
    """Stores only the latest intelligence state; never appends historical snapshots."""

    def __init__(self, database_url: str | None = None, credential_file: str | None = None):
        self.database_url = database_url or os.getenv(
            "FIREBASE_DATABASE_URL",
            "https://brainchainv227082026-default-rtdb.firebaseio.com",
        )
        self.credential_file = credential_file or os.getenv("FIREBASE_SERVICE_ACCOUNT_FILE")
        if not self.credential_file:
            raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_FILE is required")

    def write(self, analyses: list[IntelligenceAnalysis], errors: list[dict]) -> dict:
        import firebase_admin
        from firebase_admin import credentials, db

        try:
            app = firebase_admin.get_app()
        except ValueError:
            app = firebase_admin.initialize_app(
                credentials.Certificate(self.credential_file), {"databaseURL": self.database_url}
            )

        now = datetime.now(timezone.utc).isoformat()
        updates = {"market/status": {
            "last_run_at": now,
            "analysis_count": len(analyses),
            "error_count": len(errors),
            "storage_policy": "latest_state_only",
        }}
        for item in analyses:
            key = f"{item.network}:{item.token_address}:{item.pool_address}".replace("/", "_")
            updates[f"market/tokens/{key}"] = item.to_dict()

        # One multi-location update. No per-run history is appended to RTDB.
        db.reference("/", app=app).update(updates)
        return updates["market/status"]
