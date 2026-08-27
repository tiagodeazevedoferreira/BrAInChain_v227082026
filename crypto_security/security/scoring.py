from __future__ import annotations

from .models import SecurityAnalysis


def _pct(value) -> float | None:
    try:
        return float(value) * 100 if float(value) <= 1 else float(value)
    except (TypeError, ValueError):
        return None


def calculate_score(a: SecurityAnalysis) -> SecurityAnalysis:
    score = 0.0
    critical: list[str] = []
    warnings: list[str] = []

    if a.honeypot is True:
        score += 70
        critical.append("HONEYPOT_DETECTED")
    elif a.honeypot is None:
        score += 15
        warnings.append("HONEYPOT_UNKNOWN")

    if a.simulation_success is False:
        score += 12
        warnings.append("SIMULATION_FAILED")

    for field, threshold, weight, label in [
        ("sell_tax_pct", 20, 20, "EXTREME_SELL_TAX"),
        ("buy_tax_pct", 20, 10, "EXTREME_BUY_TAX"),
        ("transfer_tax_pct", 20, 10, "EXTREME_TRANSFER_TAX"),
    ]:
        value = getattr(a, field)
        if value is not None:
            if value >= threshold:
                score += weight
                critical.append(label)
            elif value >= 10:
                score += weight * 0.45
                warnings.append(label)

    if a.open_source is False or a.root_open_source is False:
        score += 18
        critical.append("CLOSED_SOURCE")
    elif a.open_source is None:
        score += 8
        warnings.append("SOURCE_STATUS_UNKNOWN")

    if a.is_proxy is True:
        score += 8
        warnings.append("PROXY_CONTRACT")
    if a.has_proxy_calls is True:
        score += 8
        warnings.append("PROXY_CALLS")

    if a.holder_sell_failures and a.analyzed_holders:
        failure_rate = a.holder_sell_failures / max(a.analyzed_holders, 1)
        if failure_rate >= 0.5:
            score += 25
            critical.append("HIGH_HOLDER_SELL_FAILURE_RATE")
        elif failure_rate > 0:
            score += 10
            warnings.append("HOLDER_SELL_FAILURES")

    if a.holder_siphoned and a.holder_siphoned > 0:
        score += 20
        critical.append("SIPHONED_HOLDERS_DETECTED")

    if a.top_holder_pct is not None:
        if a.top_holder_pct >= 50:
            score += 20
            critical.append("EXTREME_TOP_HOLDER_CONCENTRATION")
        elif a.top_holder_pct >= 25:
            score += 10
            warnings.append("HIGH_TOP_HOLDER_CONCENTRATION")

    if a.top_5_holders_pct is not None:
        if a.top_5_holders_pct >= 80:
            score += 18
            critical.append("EXTREME_TOP5_CONCENTRATION")
        elif a.top_5_holders_pct >= 60:
            score += 8
            warnings.append("HIGH_TOP5_CONCENTRATION")

    if a.liquidity_usd is not None:
        if a.liquidity_usd < 1_000:
            score += 25
            critical.append("VERY_LOW_LIQUIDITY")
        elif a.liquidity_usd < 5_000:
            score += 12
            warnings.append("LOW_LIQUIDITY")

    if a.liquidity_lock_known is False:
        score += 10
        warnings.append("LIQUIDITY_LOCK_UNKNOWN")
    elif a.liquidity_locked_pct is not None and a.liquidity_locked_pct < 50:
        score += 12
        warnings.append("LOW_LIQUIDITY_LOCK_PERCENT")

    a.risk_score = min(100.0, round(score, 2))
    a.critical_flags = sorted(set(critical))
    a.warnings = sorted(set(warnings))

    if "HONEYPOT_DETECTED" in a.critical_flags or "HIGH_HOLDER_SELL_FAILURE_RATE" in a.critical_flags:
        a.risk_level = "critical"
    elif a.risk_score >= 80:
        a.risk_level = "very_high"
    elif a.risk_score >= 60:
        a.risk_level = "high"
    elif a.risk_score >= 35:
        a.risk_level = "medium"
    elif a.risk_score >= 15:
        a.risk_level = "low"
    else:
        a.risk_level = "very_low"

    # Security is a hard gate. Unknown critical security state never becomes tradable.
    a.trade_gate = "DO_NOT_TRADE" if a.critical_flags or a.risk_score >= 35 or a.honeypot is None else "SECURITY_PASS"
    return a


def concentration_percentages(holders: list[dict], total_supply: int | float | None) -> tuple[float | None, float | None]:
    if not holders or not total_supply:
        return None, None
    try:
        supply = float(total_supply)
        balances = sorted((float(h.get("balance", 0)) for h in holders), reverse=True)
        return round(balances[0] / supply * 100, 4), round(sum(balances[:5]) / supply * 100, 4)
    except (TypeError, ValueError, ZeroDivisionError):
        return None, None
