from datetime import datetime, timezone

from .models import IntelligenceAnalysis
from .scoring import score_market, score_trades


class IntelligenceEngine:
    """Combines market and trade observations without inventing unavailable data."""

    def __init__(self, market_provider, trade_provider=None):
        self.market_provider = market_provider
        self.trade_provider = trade_provider

    def analyze(self, network: str, token_address: str, pool_address: str) -> IntelligenceAnalysis:
        flags: list[str] = []
        provider_status = {"market": "unknown", "trades": "not_configured", "holders": "not_configured"}
        features = {}

        try:
            obs = self.market_provider.observe(network, token_address, pool_address)
            provider_status["market"] = "ok"
        except Exception as exc:
            provider_status["market"] = f"error:{type(exc).__name__}"
            return IntelligenceAnalysis(
                network=network, token_address=token_address, pool_address=pool_address,
                analyzed_at=datetime.now(timezone.utc).isoformat(), market_score=0.0,
                momentum_score=0.0, liquidity_score=0.0, pressure_score=0.0,
                whale_score=0.0, smart_money_proxy_score=0.0, manipulation_risk_score=100.0,
                holder_growth_score=None, unique_traders_24h=None, buy_volume_24h_usd=None,
                sell_volume_24h_usd=None, decision="DO_NOT_TRADE",
                flags=["MARKET_PROVIDER_FAILURE"], features={}, provider_status=provider_status,
            )

        market_score, momentum, liquidity, pressure, mflags, mfeatures = score_market(obs)
        flags.extend(mflags)
        features.update(mfeatures)

        unique = None
        buy_volume = None
        sell_volume = None
        whale_score = 50.0
        smart_score = 50.0
        if self.trade_provider:
            try:
                trades = self.trade_provider.trades(network, pool_address)
                provider_status["trades"] = "ok"
                smart_score, whale_score, _, unique, buy_volume, sell_volume, tflags, tfeatures = score_trades(trades)
                flags.extend(tflags)
                features.update(tfeatures)
            except Exception as exc:
                provider_status["trades"] = f"error:{type(exc).__name__}"
                flags.append("TRADE_PROVIDER_FAILURE")
        else:
            flags.append("TRADE_PROVIDER_UNAVAILABLE")

        manipulation = 0.0
        if "SINGLE_TRADE_CONCENTRATION" in flags:
            manipulation += 45
        elif "LARGE_TRADE_CONCENTRATION" in flags:
            manipulation += 25
        if "EXTREME_LIQUIDITY_TURNOVER" in flags:
            manipulation += 25
        if "EXTREME_BUY_PRESSURE" in flags or "EXTREME_SELL_PRESSURE" in flags:
            manipulation += 20
        if "RAPID_PRICE_ACCELERATION" in flags:
            manipulation += 10
        manipulation = min(100.0, manipulation)

        # Phase 3 is intelligence, not trading. A provider gap never becomes a positive signal.
        if liquidity < 10:
            decision = "DO_NOT_TRADE"
            flags.append("LIQUIDITY_GATE")
        elif manipulation >= 70:
            decision = "DO_NOT_TRADE"
            flags.append("MANIPULATION_RISK_GATE")
        else:
            decision = "CANDIDATE"

        return IntelligenceAnalysis(
            network=network,
            token_address=token_address,
            pool_address=pool_address,
            analyzed_at=datetime.now(timezone.utc).isoformat(),
            market_score=market_score,
            momentum_score=momentum,
            liquidity_score=liquidity,
            pressure_score=pressure,
            whale_score=whale_score,
            smart_money_proxy_score=smart_score,
            manipulation_risk_score=manipulation,
            holder_growth_score=None,
            unique_traders_24h=unique,
            buy_volume_24h_usd=buy_volume,
            sell_volume_24h_usd=sell_volume,
            decision=decision,
            flags=sorted(set(flags)),
            features=features,
            provider_status=provider_status,
        )
