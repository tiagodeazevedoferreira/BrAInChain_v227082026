from crypto_ml.ml.features import build_features
from crypto_ml.ml.labels import growth_label
from crypto_ml.ml.readiness import check_readiness


def test_growth_labels():
    assert growth_label(None) == "UNKNOWN"
    assert growth_label(10) == "UP_10P"
    assert growth_label(100) == "UP_100P"
    assert growth_label(1000) == "UP_1000P"
    assert growth_label(-50) == "DOWN_CRASH"


def test_features_are_time_local():
    result = build_features({"volume_24h": 100, "liquidity_usd": 50, "buys_24h": 3, "sells_24h": 1})
    assert result["volume_liquidity_ratio"] == 2
    assert result["buy_ratio"] == 0.75


def test_readiness_blocks_small_dataset():
    ready, reasons = check_readiness([])
    assert not ready
    assert "samples<100" in reasons
    assert "unique_tokens<10" in reasons
    assert "no_labeled_samples" in reasons
