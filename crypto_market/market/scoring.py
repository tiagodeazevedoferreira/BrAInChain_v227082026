from math import log1p
from .models import MarketObservation, TradeObservation


def _clamp(value: float, low=0.0, high=100.0) -> float:
    return max(low, min(high, float(value)))


def _ratio(a: float | None, b: float | None) -> float | None:
    if a is None or b is None or b == 0:
        return None
    return a / b


def _score_ratio(ratio: float | None) -> float:
    if ratio is None:
        return 50.0
    # 1.0 = balanced. 2.0+ buys/sells is strongly positive.
    return _clamp(50.0 + 35.0 * (ratio - 1.0) / max(ratio + 1.0, 1.0))


def score_market(obs: MarketObservation) -> tuple[float, float, float, float, list[str], dict]:
    flags: list[str] = []
    features = {}

    pressure_ratio = _ratio(obs.buys_1h, obs.sells_1h)
    pressure_score = _score_ratio(pressure_ratio)

    momentum_inputs = [x for x in (obs.price_change_5m_pct, obs.price_change_1h_pct, obs.price_change_6h_pct) if x is not None]
    if momentum_inputs:
        weighted = 0.5 * (obs.price_change_5m_pct or 0) + 0.3 * (obs.price_change_1h_pct or 0) + 0.2 * (obs.price_change_6h_pct or 0)
        momentum_score = _clamp(50 + weighted * 2.0)
    else:
        momentum_score = 50.0

    if obs.liquidity_usd is None:
        liquidity_score = 0.0
        flags.append("LIQUIDITY_UNKNOWN")
    elif obs.liquidity_usd < 1_000:
        liquidity_score = 5.0
        flags.append("VERY_LOW_LIQUIDITY")
    elif obs.liquidity_usd < 10_000:
        liquidity_score = 30.0
        flags.append("LOW_LIQUIDITY")
    elif obs.liquidity_usd < 50_000:
        liquidity_score = 60.0
    elif obs.liquidity_usd < 250_000:
        liquidity_score = 80.0
    else:
        liquidity_score = 95.0

    if obs.volume_24h_usd is not None and obs.liquidity_usd:
        turnover = obs.volume_24h_usd / max(obs.liquidity_usd, 1.0)
        features["liquidity_turnover_24h"] = turnover
        if turnover > 20:
            flags.append("EXTREME_LIQUIDITY_TURNOVER")
        elif turnover > 8:
            flags.append("HIGH_LIQUIDITY_TURNOVER")

    if obs.price_change_1h_pct is not None and obs.price_change_24h_pct is not None:
        acceleration = obs.price_change_1h_pct - (obs.price_change_24h_pct / 24.0)
        features["price_acceleration_proxy"] = acceleration
        if acceleration > 25:
            flags.append("RAPID_PRICE_ACCELERATION")

    if pressure_ratio is not None:
        features["buy_sell_ratio_1h"] = pressure_ratio
    if obs.volume_1h_usd is not None and obs.volume_24h_usd:
        features["volume_share_1h"] = obs.volume_1h_usd / max(obs.volume_24h_usd, 1.0)

    if obs.buys_1h is not None and obs.sells_1h is not None and obs.buys_1h + obs.sells_1h > 0:
        buy_share = obs.buys_1h / (obs.buys_1h + obs.sells_1h)
        features["buy_transaction_share_1h"] = buy_share
        if buy_share > 0.85:
            flags.append("EXTREME_BUY_PRESSURE")
        elif buy_share < 0.20:
            flags.append("EXTREME_SELL_PRESSURE")

    market_score = _clamp(
        0.35 * momentum_score + 0.25 * pressure_score + 0.25 * liquidity_score + 0.15 * (70.0 if obs.volume_24h_usd else 40.0)
    )
    return market_score, momentum_score, liquidity_score, pressure_score, flags, features


def score_trades(trades: list[TradeObservation]) -> tuple[float, float, float, int | None, float | None, float | None, list[str], dict]:
    if not trades:
        return 50.0, 50.0, 50.0, None, None, None, ["TRADE_DATA_UNAVAILABLE"], {}

    valid = [t for t in trades if t.volume_usd is not None]
    buyers = [t for t in valid if (t.side or "").startswith("buy")]
    sellers = [t for t in valid if (t.side or "").startswith("sell")]
    buy_volume = sum(t.volume_usd or 0 for t in buyers) or None
    sell_volume = sum(t.volume_usd or 0 for t in sellers) or None
    traders = {t.trader_address.lower() for t in trades if t.trader_address}
    unique = len(traders) or None

    whale_score = 50.0
    smart_score = 50.0
    flags: list[str] = []
    features: dict = {}
    if valid:
        total = sum(t.volume_usd or 0 for t in valid)
        largest = max((t.volume_usd or 0) for t in valid)
        concentration = largest / total if total else None
        features["largest_trade_share"] = concentration
        if concentration is not None:
            whale_score = _clamp(100 - concentration * 100)
            if concentration > 0.50:
                flags.append("SINGLE_TRADE_CONCENTRATION")
            elif concentration > 0.30:
                flags.append("LARGE_TRADE_CONCENTRATION")

        if buy_volume is not None and sell_volume is not None:
            net = (buy_volume - sell_volume) / max(buy_volume + sell_volume, 1.0)
            smart_score = _clamp(50 + net * 50)
            features["trade_net_buy_ratio"] = net

    return smart_score, whale_score, smart_score, unique, buy_volume, sell_volume, flags, features
