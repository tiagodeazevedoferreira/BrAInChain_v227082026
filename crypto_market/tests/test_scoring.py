from market.models import MarketObservation, TradeObservation
from market.scoring import score_market, score_trades


def test_market_scoring_detects_buy_pressure_and_acceleration():
    obs = MarketObservation(
        network="solana", token_address="T", pool_address="P", dex_id="dex", symbol="T",
        price_usd=1.0, liquidity_usd=100_000, volume_1h_usd=80_000,
        volume_24h_usd=200_000, buys_1h=90, sells_1h=10,
        price_change_5m_pct=12, price_change_1h_pct=40, price_change_6h_pct=60,
    )
    market, momentum, liquidity, pressure, flags, features = score_market(obs)
    assert market > 60
    assert momentum > 50
    assert liquidity >= 80
    assert pressure > 50
    assert "EXTREME_BUY_PRESSURE" in flags
    assert features["buy_transaction_share_1h"] == 0.9


def test_trade_scoring_is_conservative_when_data_is_missing():
    smart, whale, _, unique, buy, sell, flags, _ = score_trades([])
    assert smart == 50
    assert whale == 50
    assert unique is None
    assert buy is None
    assert sell is None
    assert "TRADE_DATA_UNAVAILABLE" in flags


def test_trade_scoring_detects_concentration_and_net_buying():
    trades = [
        TradeObservation(1, "buy", 1000, 1, "A", "tx1"),
        TradeObservation(2, "buy", 500, 1.1, "B", "tx2"),
        TradeObservation(3, "sell", 100, 1.2, "C", "tx3"),
    ]
    smart, whale, _, unique, buy, sell, flags, features = score_trades(trades)
    assert unique == 3
    assert buy == 1500
    assert sell == 100
    assert smart > 50
    assert whale < 50  # lower score means higher single-trade concentration risk
    assert "SINGLE_TRADE_CONCENTRATION" in flags
    assert features["trade_net_buy_ratio"] > 0
