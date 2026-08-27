from .models import PositionSnapshot


def build_signal_snapshot(raw: dict) -> PositionSnapshot:
    """Normalize paper-market observations into the exit contract."""
    return PositionSnapshot(
        token_id=str(raw["token_id"]),
        entry_price=float(raw["entry_price"]),
        current_price=float(raw["current_price"]),
        peak_price=float(raw.get("peak_price", raw["current_price"])),
        entry_timestamp=str(raw["entry_timestamp"]),
        current_timestamp=str(raw["current_timestamp"]),
        liquidity_usd=float(raw.get("liquidity_usd", 0)),
        momentum_score=float(raw.get("momentum_reversal_score", 0)),
        volume_reversal_score=float(raw.get("volume_reversal_score", 0)),
        sell_pressure_score=float(raw.get("sell_pressure_score", 0)),
        whale_exit_score=float(raw.get("whale_exit_score", 0)),
        crash_risk_score=float(raw.get("crash_risk_score", 0)),
    )
