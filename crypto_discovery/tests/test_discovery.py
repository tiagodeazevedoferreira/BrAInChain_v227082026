from datetime import datetime, timezone

from discovery.adapters import CompositeDiscovery
from discovery.models import DiscoveredPool
from discovery.service import DiscoveryService


def pool(address="0xpool"):
    return DiscoveredPool(
        source="fake",
        network="eth",
        pool_address=address,
        base_token_address="0xtoken",
        base_token_symbol="T",
        base_token_name="Token",
        quote_token_address="0xquote",
        quote_token_symbol="Q",
        quote_token_name="Quote",
        dex_id="dex",
        pool_created_at=None,
        price_usd=None,
        liquidity_usd=None,
        fdv_usd=None,
        volume_24h_usd=None,
        discovered_at=datetime.now(timezone.utc),
        source_payload={},
    )


class FakeAdapter:
    source = "fake"

    def __init__(self, items):
        self.items = items

    def discover(self):
        return self.items


def test_composite_deduplicates_same_observation():
    result = DiscoveryService(
        CompositeDiscovery([FakeAdapter([pool()]), FakeAdapter([pool()])])
    ).run()
    assert len(result.pools) == 1
    assert result.errors == []


def test_composite_isolates_source_failure():
    class BrokenAdapter:
        source = "broken"

        def discover(self):
            raise RuntimeError("boom")

    result = DiscoveryService(
        CompositeDiscovery([BrokenAdapter(), FakeAdapter([pool()])])
    ).run()
    assert len(result.pools) == 1
    assert result.errors == [{"source": "broken", "error": "boom"}]


def test_model_serializes_datetime():
    value = pool().to_dict()
    assert isinstance(value["discovered_at"], str)
    assert value["network"] == "eth"
