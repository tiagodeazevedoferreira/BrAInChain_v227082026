from discovery.adapters import DexScreenerAdapter, GeckoTerminalAdapter


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        for needle, payload in self.responses:
            if needle in url:
                return FakeResponse(payload)
        raise AssertionError(f"Unexpected URL: {url}")


def test_geckoterminal_normalizes_new_pool():
    session = FakeSession(
        [
            (
                "/networks/new_pools",
                {
                    "data": [
                        {
                            "id": "eth_0xpool",
                            "attributes": {
                                "address": "0xpool",
                                "pool_created_at": "2026-08-27T20:00:00Z",
                                "base_token_price_usd": "0.001",
                                "reserve_in_usd": "1234.50",
                                "fdv_usd": "10000",
                                "volume_usd": {"h24": "321.5"},
                            },
                            "relationships": {
                                "base_token": {"data": {"id": "eth_0xtoken"}},
                                "quote_token": {"data": {"id": "eth_0xquote"}},
                                "dex": {"data": {"id": "uniswap_v3"}},
                            },
                        }
                    ],
                    "included": [
                        {"id": "eth_0xtoken", "attributes": {"address": "0xtoken", "symbol": "NEW", "name": "New"}},
                        {"id": "eth_0xquote", "attributes": {"address": "0xquote", "symbol": "WETH", "name": "Wrapped Ether"}},
                    ],
                },
            )
        ]
    )
    result = GeckoTerminalAdapter(session=session, pages=1).discover()
    assert len(result) == 1
    assert result[0].network == "eth"
    assert result[0].base_token_address == "0xtoken"
    assert result[0].liquidity_usd == 1234.5
    assert result[0].volume_24h_usd == 321.5


def test_dexscreener_normalizes_pair():
    session = FakeSession(
        [
            ("/token-profiles/latest/v1", [{"chainId": "solana", "tokenAddress": "TOKEN"}]),
            (
                "/tokens/v1/solana/TOKEN",
                [
                    {
                        "pairAddress": "PAIR",
                        "pairCreatedAt": 1756324800000,
                        "baseToken": {"address": "TOKEN", "symbol": "NEW", "name": "New"},
                        "quoteToken": {"address": "QUOTE", "symbol": "SOL", "name": "Solana"},
                        "dexId": "raydium",
                        "priceUsd": "0.02",
                        "liquidity": {"usd": 2500},
                        "fdv": 15000,
                        "volume": {"h24": 7000},
                    }
                ],
            ),
        ]
    )
    result = DexScreenerAdapter(session=session).discover()
    assert len(result) == 1
    assert result[0].network == "solana"
    assert result[0].pool_address == "PAIR"
    assert result[0].price_usd == 0.02
    assert result[0].liquidity_usd == 2500.0
