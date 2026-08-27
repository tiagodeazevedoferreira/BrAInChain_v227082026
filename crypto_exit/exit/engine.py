from .models import ExitConfig, ExitDecision, PositionSnapshot


def evaluate(snapshot: PositionSnapshot, config: ExitConfig | None = None) -> ExitDecision:
    config = config or ExitConfig()
    if snapshot.entry_price <= 0 or snapshot.current_price <= 0 or snapshot.peak_price <= 0:
        return ExitDecision(True, "invalid_price", 100.0, 0.0)

    gain_pct = (snapshot.current_price / snapshot.entry_price - 1.0) * 100.0
    drawdown_from_peak = (1.0 - snapshot.current_price / snapshot.peak_price) * 100.0
    peak_capture = snapshot.current_price / snapshot.peak_price * 100.0
    age_seconds = _parse_seconds(snapshot.entry_timestamp, snapshot.current_timestamp)
    age_minutes = age_seconds / 60.0

    signals = {
        "momentum_reversal": snapshot.momentum_score,
        "volume_reversal": snapshot.volume_reversal_score,
        "sell_pressure": snapshot.sell_pressure_score,
        "whale_exit": snapshot.whale_exit_score,
        "crash_risk": snapshot.crash_risk_score,
    }
    exit_score = sum(signals.values()) / len(signals)

    if snapshot.liquidity_usd < config.liquidity_floor_usd:
        return ExitDecision(True, "liquidity_deterioration", exit_score, peak_capture)
    if drawdown_from_peak >= config.trailing_stop_pct:
        return ExitDecision(True, "trailing_stop", exit_score, peak_capture)
    if gain_pct >= config.take_profit_pct and exit_score >= config.reversal_score_threshold:
        return ExitDecision(True, "take_profit_with_reversal", exit_score, peak_capture)
    if exit_score >= config.reversal_score_threshold:
        return ExitDecision(True, "reversal_risk", exit_score, peak_capture)
    if age_minutes >= config.max_hold_minutes:
        return ExitDecision(True, "time_stop", exit_score, peak_capture)
    return ExitDecision(False, "hold", exit_score, peak_capture)


def _parse_seconds(start: str, end: str) -> float:
    from datetime import datetime
    a = datetime.fromisoformat(start.replace("Z", "+00:00"))
    b = datetime.fromisoformat(end.replace("Z", "+00:00"))
    return max(0.0, (b - a).total_seconds())
