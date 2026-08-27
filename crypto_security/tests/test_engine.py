from security.engine import SecurityEngine


class FakeHoneypot:
    def check(self, address, network, pair=None):
        return {
            "token": {"totalHolders": 100},
            "summary": {"risk": "low", "riskLevel": 5},
            "simulationSuccess": True,
            "honeypotResult": {"isHoneypot": False},
            "simulationResult": {"buyTax": 2, "sellTax": 3, "transferTax": 0},
            "holderAnalysis": {"holders": "10", "failed": "0", "siphoned": "0"},
            "contractCode": {"openSource": True, "rootOpenSource": True, "isProxy": False, "hasProxyCalls": False},
        }

    def top_holders(self, address, network):
        return {"totalSupply": "1000", "holders": [{"balance": "100"}, {"balance": "50"}]}

    def contract_verification(self, address, network):
        return {"isRootOpenSource": True, "summary": {"isOpenSource": True, "hasProxyCalls": False}}


class FakeGoPlus:
    enabled = False


def test_engine_uses_all_local_checks():
    result = SecurityEngine(FakeHoneypot(), FakeGoPlus()).analyze(
        {
            "network": "1",
            "base_token_address": "0xabc",
            "base_token_symbol": "TEST",
            "base_token_name": "Test",
            "pool_address": "0xpool",
            "liquidity_usd": 100_000,
        }
    )
    assert result.honeypot is False
    assert result.buy_tax_pct == 2
    assert result.sell_tax_pct == 3
    assert result.open_source is True
    assert result.top_holder_pct == 10
    assert result.trade_gate == "SECURITY_PASS"
