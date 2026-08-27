from exit.engine import evaluate
from exit.models import ExitConfig, PositionSnapshot


def snap(**kw):
    base = dict(token_id="x", entry_price=1, current_price=1.5, peak_price=1.5,
                entry_timestamp="2026-01-01T00:00:00+00:00", current_timestamp="2026-01-01T00:30:00+00:00",
                liquidity_usd=1000, momentum_score=10, volume_reversal_score=10,
                sell_pressure_score=10, whale_exit_score=10, crash_risk_score=10)
    base.update(kw)
    return PositionSnapshot(**base)


def test_hold_when_signals_are_healthy():
    d = evaluate(snap())
    assert not d.should_exit
    assert d.reason == "hold"


def test_trailing_stop():
    d = evaluate(snap(current_price=1.1, peak_price=1.5))
    assert d.should_exit and d.reason == "trailing_stop"


def test_liquidity_floor_has_priority():
    d = evaluate(snap(liquidity_usd=50))
    assert d.should_exit and d.reason == "liquidity_deterioration"


def test_reversal_exit():
    d = evaluate(snap(momentum_score=90, volume_reversal_score=90, sell_pressure_score=80, whale_exit_score=70, crash_risk_score=80))
    assert d.should_exit
    assert d.exit_score >= 70


def test_time_stop():
    d = evaluate(snap(current_timestamp="2026-01-02T00:00:01+00:00"), ExitConfig(max_hold_minutes=1440))
    assert d.should_exit and d.reason == "time_stop"
