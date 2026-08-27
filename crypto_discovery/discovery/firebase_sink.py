import os
from datetime import datetime, timezone
from typing import Iterable

from .models import DiscoveredPool


class FirebaseDiscoverySink:
    """Persists discovery observations and run status in Firebase RTDB."""

    def __init__(self, database_url: str | None = None, credential_file: str | None = None):
        self.database_url = database_url or os.getenv(
            "FIREBASE_DATABASE_URL",
            "https://brainchainv227082026-default-rtdb.firebaseio.com",
        )
        self.credential_file = credential_file or os.getenv("FIREBASE_SERVICE_ACCOUNT_FILE")
        if not self.credential_file:
            raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_FILE is required")

    def write(self, pools: Iterable[DiscoveredPool], errors: list[dict]):
        import firebase_admin
        from firebase_admin import credentials, db

        try:
            app = firebase_admin.get_app()
        except ValueError:
            app = firebase_admin.initialize_app(
                credentials.Certificate(self.credential_file),
                {"databaseURL": self.database_url},
            )

        pool_list = list(pools)
        payload = {
            "last_run_at": datetime.now(timezone.utc).isoformat(),
            "pool_count": len(pool_list),
            "source_errors": errors,
        }

        for pool in pool_list:
            key = f"{pool.network}:{pool.base_token_address or 'unknown'}:{pool.pool_address or 'unknown'}"
            key = key.replace("/", "_")
            db.reference(f"discovery/tokens/{key}", app=app).set(pool.to_dict())

        db.reference("discovery/status", app=app).set(payload)
        return payload
