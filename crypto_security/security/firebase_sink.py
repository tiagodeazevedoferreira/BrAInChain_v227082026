import os
from datetime import datetime, timezone

from .models import SecurityAnalysis


class FirebaseSecuritySink:
    def __init__(self, database_url: str | None = None, credential_file: str | None = None):
        self.database_url = database_url or os.getenv(
            "FIREBASE_DATABASE_URL",
            "https://brainchainv227082026-default-rtdb.firebaseio.com",
        )
        self.credential_file = credential_file or os.getenv("FIREBASE_SERVICE_ACCOUNT_FILE")
        if not self.credential_file:
            raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_FILE is required")

    def write(self, analyses: list[SecurityAnalysis], errors: list[dict]) -> dict:
        import firebase_admin
        from firebase_admin import credentials, db

        try:
            app = firebase_admin.get_app()
        except ValueError:
            app = firebase_admin.initialize_app(
                credentials.Certificate(self.credential_file),
                {"databaseURL": self.database_url},
            )

        updates = {}
        for analysis in analyses:
            key = f"{analysis.network}:{analysis.token_address}:{analysis.pool_address or 'unknown'}".replace("/", "_")
            updates[f"security/tokens/{key}"] = analysis.to_dict()

        updates["security/status"] = {
            "last_run_at": datetime.now(timezone.utc).isoformat(),
            "token_count": len(analyses),
            "critical_count": sum(bool(a.critical_flags) for a in analyses),
            "do_not_trade_count": sum(a.trade_gate == "DO_NOT_TRADE" for a in analyses),
            "errors": errors,
        }
        db.reference("/", app=app).update(updates)
        return updates["security/status"]
