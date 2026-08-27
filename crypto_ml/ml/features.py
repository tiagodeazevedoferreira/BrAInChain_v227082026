"""Feature extraction from normalized market/security observations."""


def build_features(observation: dict) -> dict[str, float]:
    def num(name: str) -> float:
        value = observation.get(name)
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    volume = num("volume_24h")
    liquidity = num("liquidity_usd")
    buys = num("buys_24h")
    sells = num("sells_24h")
    total_trades = buys + sells
    return {
        "price_usd": num("price_usd"),
        "volume_24h": volume,
        "liquidity_usd": liquidity,
        "volume_liquidity_ratio": volume / liquidity if liquidity > 0 else 0.0,
        "buy_ratio": buys / total_trades if total_trades > 0 else 0.0,
        "momentum_score": num("momentum_score"),
        "pressure_score": num("pressure_score"),
        "whale_score": num("whale_score"),
        "smart_money_proxy_score": num("smart_money_proxy_score"),
        "security_score": num("security_score"),
        "manipulation_risk_score": num("manipulation_risk_score"),
    }
