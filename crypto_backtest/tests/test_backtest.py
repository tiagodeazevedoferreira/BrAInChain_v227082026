from backtest.engine import run
from backtest.metrics import summarize
from backtest.models import BacktestConfig, MarketEvent


def event(ts, price, score=90, security=True, liquidity=1000):
    return MarketEvent(ts, "token", price, liquidity, score, security)


def test_security_gate_blocks_trade():
    trades = run([event("2026-01-01T00:00:00", 1, security=False), event("2026-01-01T01:00:00", 2)])
    assert trades == []


def test_score_and_liquidity_gate():
    trades = run([event("2026-01-01T00:00:00", 1, score=50), event("2026-01-01T01:00:00", 2)])
    assert trades == []


def test_net_pnl_includes_fee_and_slippage():
    trades = run([event("2026-01-01T00:00:00", 1), event("2026-01-01T01:00:00", 2)], BacktestConfig(fee_bps=100, slippage_bps=100))
    assert len(trades) == 1
    assert trades[0].net_pnl_usd < 0.01


def test_metrics():
    trades = run([event("2026-01-01T00:00:00", 1), event("2026-01-01T01:00:00", 2)])
    summary = summarize(trades)
    assert summary["trades"] == 1
    assert summary["wins"] == 1
