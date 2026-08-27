from paper.executor import PaperExecutor
from paper.models import PaperConfig, PaperSignal


def signal(**kwargs):
    data = dict(timestamp="2026-08-27T12:00:00Z", token_id="token", price_usd=1.0, liquidity_usd=10000, opportunity_score=90, security_gate="SECURITY_PASS", signal="BUY")
    data.update(kwargs)
    return PaperSignal(**data)


def test_buy_is_simulated_and_uses_target_capital():
    ex = PaperExecutor(PaperConfig(initial_capital_usd=1.0, position_target_usd=0.01))
    result, position = ex.process_signal(signal())
    assert result == "PAPER_BUY_FILLED"
    assert position is not None
    assert ex.cash_usd < 1.0
    assert len(ex.positions) == 1


def test_security_gate_cannot_be_overridden():
    ex = PaperExecutor(PaperConfig(initial_capital_usd=1.0))
    result, position = ex.process_signal(signal(security_gate="DO_NOT_TRADE"))
    assert result == "DO_NOT_TRADE_SECURITY_GATE"
    assert position is None


def test_close_realizes_net_pnl():
    ex = PaperExecutor(PaperConfig(initial_capital_usd=1.0, position_target_usd=0.01, fee_bps=0, slippage_bps=0))
    _, position = ex.process_signal(signal())
    closed = ex.close(position.position_id, "2026-08-27T13:00:00Z", 2.0, "TEST_EXIT")
    assert closed.status == "CLOSED"
    assert closed.realized_pnl_usd > 0


def test_daily_loss_circuit_breaker():
    config = PaperConfig(initial_capital_usd=1.0, position_target_usd=0.01, daily_loss_limit_usd=0.001)
    ex = PaperExecutor(config)
    _, position = ex.process_signal(signal())
    ex.close(position.position_id, "2026-08-27T13:00:00Z", 0.5, "LOSS")
    assert ex.risk.halted
    assert ex.risk.halt_reason == "DAILY_LOSS_LIMIT"
