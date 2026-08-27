from paper.models import PaperPosition
from paper.monitor import snapshot


def test_monitor_reports_open_value_and_unrealized_pnl():
    position = PaperPosition("1", "TOKEN", "2026-08-27T12:00:00Z", 1.0, 0.01, 0.01, 0.0)
    result = snapshot([position], {"TOKEN": 2.0})
    assert result["open_positions"] == 1
    assert result["market_value_usd"] == 0.02
    assert result["unrealized_pnl_usd"] == 0.01
