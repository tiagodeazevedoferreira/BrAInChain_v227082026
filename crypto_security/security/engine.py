from __future__ import annotations

from typing import Any

from .models import SecurityAnalysis
from .providers import GoPlusProvider, HoneypotProvider, chain_id
from .scoring import calculate_score, concentration_percentages


class SecurityEngine:
    """Runs layered security checks. Provider failure is recorded, never hidden."""

    def __init__(self, honeypot=None, goplus=None):
        self.honeypot = honeypot or HoneypotProvider()
        self.goplus = goplus or GoPlusProvider()

    def analyze(self, pool: dict[str, Any]) -> SecurityAnalysis:
        token = pool.get("base_token_address")
        network = pool.get("network", "unknown")
        result = SecurityAnalysis(
            network=network,
            token_address=token or "",
            pool_address=pool.get("pool_address"),
            symbol=pool.get("base_token_symbol"),
            name=pool.get("base_token_name"),
            liquidity_usd=self._float(pool.get("liquidity_usd")),
        )
        if not token:
            result.critical_flags.append("MISSING_TOKEN_ADDRESS")
            result.provider_status["engine"] = "invalid_input"
            return calculate_score(result)

        if chain_id(network) is None:
            result.provider_status["honeypot_is"] = "unsupported_chain"
            result.provider_status["goplus"] = "unsupported_chain"
            result.warnings.append("CHAIN_NOT_SUPPORTED_BY_SECURITY_PROVIDERS")
            result.risk_score = 100.0
            result.risk_level = "unknown"
            result.trade_gate = "DO_NOT_TRADE"
            return result

        try:
            hp = self.honeypot.check(token, network, pool.get("pool_address"))
            result.provider_status["honeypot_is"] = "ok"
            result.evidence["honeypot_is"] = hp
            result.honeypot = self._bool(hp.get("honeypotResult", {}).get("isHoneypot"))
            result.honeypot_reason = hp.get("honeypotResult", {}).get("honeypotReason")
            result.simulation_success = self._bool(hp.get("simulationSuccess"))
            sim = hp.get("simulationResult") or {}
            result.buy_tax_pct = self._float(sim.get("buyTax"))
            result.sell_tax_pct = self._float(sim.get("sellTax"))
            result.transfer_tax_pct = self._float(sim.get("transferTax"))
            code = hp.get("contractCode") or {}
            result.open_source = self._bool(code.get("openSource"))
            result.root_open_source = self._bool(code.get("rootOpenSource"))
            result.is_proxy = self._bool(code.get("isProxy"))
            result.has_proxy_calls = self._bool(code.get("hasProxyCalls"))
            token_info = hp.get("token") or {}
            result.holder_count = self._int(token_info.get("totalHolders"))
            ha = hp.get("holderAnalysis") or {}
            result.analyzed_holders = self._int(ha.get("holders"))
            result.holder_sell_failures = self._int(ha.get("failed"))
            result.holder_siphoned = self._int(ha.get("siphoned"))
        except Exception as exc:
            result.provider_status["honeypot_is"] = f"error:{type(exc).__name__}"
            result.evidence["honeypot_is_error"] = str(exc)

        try:
            holders = self.honeypot.top_holders(token, network)
            result.provider_status["top_holders"] = "ok"
            result.evidence["top_holders"] = holders
            top, top5 = concentration_percentages(holders.get("holders", []), holders.get("totalSupply"))
            result.top_holder_pct = top
            result.top_5_holders_pct = top5
        except Exception as exc:
            result.provider_status["top_holders"] = f"error:{type(exc).__name__}"
            result.evidence["top_holders_error"] = str(exc)

        try:
            verification = self.honeypot.contract_verification(token, network)
            result.provider_status["contract_verification"] = "ok"
            result.evidence["contract_verification"] = verification
            if "isRootOpenSource" in verification:
                result.root_open_source = self._bool(verification["isRootOpenSource"])
            summary = verification.get("summary") or {}
            if "isOpenSource" in summary:
                result.open_source = self._bool(summary["isOpenSource"])
            if "hasProxyCalls" in summary:
                result.has_proxy_calls = self._bool(summary["hasProxyCalls"])
        except Exception as exc:
            result.provider_status["contract_verification"] = f"error:{type(exc).__name__}"
            result.evidence["contract_verification_error"] = str(exc)

        if self.goplus.enabled:
            try:
                gp = self.goplus.token_security(token, network)
                result.provider_status["goplus"] = "ok"
                result.evidence["goplus"] = gp
                self._merge_goplus(result, gp)
            except Exception as exc:
                result.provider_status["goplus"] = f"error:{type(exc).__name__}"
                result.evidence["goplus_error"] = str(exc)
        else:
            result.provider_status["goplus"] = "not_configured"

        return calculate_score(result)

    @staticmethod
    def _merge_goplus(result: SecurityAnalysis, gp: dict[str, Any]) -> None:
        mapping = {
            "is_honeypot": "honeypot",
            "is_open_source": "open_source",
            "is_proxy": "is_proxy",
            "buy_tax": "buy_tax_pct",
            "sell_tax": "sell_tax_pct",
            "transfer_tax": "transfer_tax_pct",
            "holder_count": "holder_count",
        }
        for source, target in mapping.items():
            if source in gp:
                value = gp[source]
                if target.endswith("_pct"):
                    value = SecurityEngine._float(value)
                    if value is not None and value <= 1:
                        value *= 100
                elif target in {"honeypot", "open_source", "is_proxy"}:
                    value = SecurityEngine._bool(value)
                elif target == "holder_count":
                    value = SecurityEngine._int(value)
                if value is not None:
                    setattr(result, target, value)
        if gp.get("is_honeypot") in ("1", 1, True):
            result.honeypot = True

    @staticmethod
    def _float(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _int(value):
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _bool(value):
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        return str(value).lower() in {"1", "true", "yes"}
