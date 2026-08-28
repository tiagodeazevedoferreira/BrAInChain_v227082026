from monitoring.metrics import classification_metrics, default_targets
from monitoring.readiness import evaluate_readiness


def test_metrics():
    m = classification_metrics(60, 40, 20, 80)
    assert round(m["precision"], 2) == 60.0
    assert round(m["recall"], 2) == 75.0
    assert m["balanced_accuracy"] > 60


def test_targets_have_evolution_goals():
    assert {x.key for x in default_targets()} >= {"precision", "recall", "balanced_accuracy", "mean_return_pct", "max_drawdown_pct", "peak_capture_pct"}


def test_readiness_is_fail_closed():
    r = evaluate_readiness(data_quality=True, sufficient_samples=True, oos_validated=True,
                           walk_forward_validated=True, paper_trading_validated=True,
                           security_validated=True, failure_tests_validated=True,
                           secrets_validated=True, circuit_breakers_validated=True)
    assert not r.ready
    assert any(g.key == "venue" and not g.passed for g in r.gates)
