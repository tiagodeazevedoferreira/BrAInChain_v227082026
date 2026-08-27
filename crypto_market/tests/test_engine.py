from market.engine import IntelligenceEngine
from market.models import MarketObservation, TradeObservation


class FakeMarket:
    def observe(self, network, token_address, pool_address):
        return MarketObservation(
            network, token_address, pool_address, "dex", "T",
            price_usd=1, liquidity_usd=100_000, volume_1h_usd=20_000,
            volume_24h_usd=100_000, buys_1h=60, sells_1h=40,
            price_change_5m_pct=3, price_change_1h_pct=10, price_change_6h_pct=20,
        )


class FakeTrades:
    def trades(self, network, pool_address):
        return [TradeObservation(1, "buy", 100, 1, "A", "x")]


def test_engine_returns_candidate_without_trade_execution():
    result = IntelligenceEngine(FakeMarket(), FakeTrades()).analyze("solana", "T", "P")
    assert result.decision == "CANDIDATE"
    assert result.provider_status["market"] == "ok"
    assert result.provider_status["trades"] == "ok"
    assert result.market_score > 0


def test_engine_fails_closed_when_market_provider_fails():
    class Broken:
        def observe(self, *args):
            raise RuntimeError("down")

    result = IntelligenceEngine(Broken()).analyze("solana", "T", "P")
    assert result.decision == "DO_NOT_TRADE"
    assert "MARKET_PROVIDER_FAILURE" in result.flags
