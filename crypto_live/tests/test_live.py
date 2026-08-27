from live.config import LiveConfig
from live.executor import LiveExecutor
from live.gates import Evidence, preflight


def test_default_configuration_cannot_go_live():
    ok, failures = preflight(LiveConfig(), Evidence())
    assert not ok
    assert "LIVE_TRADING_DISABLED" in failures
    assert "OWNER_AUTHORIZATION_REQUIRED" in failures


def test_missing_evidence_blocks_even_when_configured():
    config = LiveConfig(trading_mode="live", live_trading_enabled=True, owner_authorized=True)
    ok, failures = preflight(config, Evidence())
    assert not ok
    assert "BACKTEST_EVIDENCE_REQUIRED" in failures
    assert "OUT_OF_SAMPLE_EVIDENCE_REQUIRED" in failures
    assert "PAPER_EVIDENCE_REQUIRED" in failures


def test_executor_fails_closed():
    assert LiveExecutor(False).submit({"side": "BUY"})["status"] == "BLOCKED"
    assert LiveExecutor(True).submit({"side": "BUY"})["reason"] == "NO_APPROVED_VENUE_ADAPTER"
