from __future__ import annotations
import os


def float_env(name: str, default: float) -> float:
    value = os.getenv(name)
    return default if value is None else float(value)


def monitoring_config() -> dict:
    return {
        "refresh_seconds": int(os.getenv("MONITOR_REFRESH_SECONDS", "300")),
        "paper_refresh_seconds": int(os.getenv("PAPER_REFRESH_SECONDS", "60")),
        "candidate_trade_usd": float_env("TARGET_TRADE_USD", 0.01),
        "max_exposure_usd": float_env("MAX_EXPOSURE_USD", 0.10),
        "dashboard_mode": os.getenv("DASHBOARD_MODE", "monitoring"),
    }
