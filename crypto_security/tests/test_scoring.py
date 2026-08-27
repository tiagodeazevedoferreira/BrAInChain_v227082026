from security.models import SecurityAnalysis
from security.scoring import calculate_score, concentration_percentages


def test_honeypot_is_hard_block():
    result = calculate_score(SecurityAnalysis(network="1", token_address="0x1", honeypot=True))
    assert result.risk_score >= 70
    assert result.trade_gate == "DO_NOT_TRADE"
    assert "HONEYPOT_DETECTED" in result.critical_flags


def test_unknown_security_cannot_trade():
    result = calculate_score(SecurityAnalysis(network="1", token_address="0x1"))
    assert result.trade_gate == "DO_NOT_TRADE"


def test_concentration():
    top, top5 = concentration_percentages(
        [{"balance": "600"}, {"balance": "100"}, {"balance": "50"}],
        "1000",
    )
    assert top == 60.0
    assert top5 == 75.0
