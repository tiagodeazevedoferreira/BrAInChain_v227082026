from abc import ABC, abstractmethod
from typing import Any
import requests

from .models import MarketObservation, TradeObservation


class MarketProvider(ABC):
    name = "unknown"

    @abstractmethod
    def observe(self, network: str, token_address: str, pool_address: str) -> MarketObservation:
        raise NotImplementedError


class TradeProvider(ABC):
    name = "unknown"

    @abstractmethod
    def trades(self, network: str, pool_address: str) -> list[TradeObservation]:
        raise NotImplementedError


def _float(value):
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _int(value):
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _first(mapping: dict[str, Any], *keys):
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return None


def _period(mapping: dict[str, Any], period: str, field: str):
    obj = mapping.get(field) or {}
    return _first(obj, period)


class DexScreenerMarketProvider(MarketProvider):
    name = "dexscreener"
    base_url = "https://api.dexscreener.com"

    def __init__(self, session=None, timeout: int = 20):
        self.session = session or requests.Session()
        self.timeout = timeout

    def observe(self, network: str, token_address: str, pool_address: str) -> MarketObservation:
        response = self.session.get(
            f"{self.base_url}/latest/dex/pairs/{network}/{pool_address}", timeout=self.timeout
        )
        response.raise_for_status()
        pairs = (response.json() or {}).get("pairs") or []
        pair = next((p for p in pairs if p.get("pairAddress", '').lower() == pool_address.lower()), None)
        if pair is None and pairs:
            pair = pairs[0]
        if not pair:
            raise ValueError("DEX Screener returned no pair")

        txns = pair.get("txns") or {}
        volume = pair.get("volume") or {}
        changes = pair.get("priceChange") or {}
        liquidity = pair.get("liquidity") or {}
        boosts = pair.get("boosts") or {}
        base = pair.get("baseToken") or {}

        return MarketObservation(
            network=network,
            token_address=token_address,
            pool_address=pool_address,
            dex_id=pair.get("dexId"),
            symbol=base.get("symbol"),
            price_usd=_float(pair.get("priceUsd")),
            liquidity_usd=_float(liquidity.get("usd")),
            volume_1h_usd=_float(volume.get("h1")),
            volume_6h_usd=_float(volume.get("h6")),
            volume_24h_usd=_float(volume.get("h24")),
            buys_1h=_int(_period(txns, "h1", "buys")),
            sells_1h=_int(_period(txns, "h1", "sells")),
            buys_6h=_int(_period(txns, "h6", "buys")),
            sells_6h=_int(_period(txns, "h6", "sells")),
            buys_24h=_int(_period(txns, "h24", "buys")),
            sells_24h=_int(_period(txns, "h24", "sells")),
            price_change_5m_pct=_float(changes.get("m5")),
            price_change_1h_pct=_float(changes.get("h1")),
            price_change_6h_pct=_float(changes.get("h6")),
            price_change_24h_pct=_float(changes.get("h24")),
            fdv_usd=_float(pair.get("fdv")),
            market_cap_usd=_float(pair.get("marketCap")),
            boosts_active=_int(boosts.get("active")),
            raw_source="dexscreener",
        )


class GeckoTerminalTradeProvider(TradeProvider):
    name = "geckoterminal"
    base_url = "https://api.geckoterminal.com/api/v2"

    def __init__(self, session=None, timeout: int = 20):
        self.session = session or requests.Session()
        self.timeout = timeout

    def trades(self, network: str, pool_address: str) -> list[TradeObservation]:
        response = self.session.get(
            f"{self.base_url}/networks/{network}/pools/{pool_address}/trades",
            headers={"Accept": "application/json;version=20230203"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        rows = (response.json() or {}).get("data") or []
        result = []
        for row in rows:
            a = row.get("attributes") or {}
            side = str(_first(a, "kind", "side", "type") or "").lower() or None
            volume = _float(_first(a, "volume_in_usd", "volume_usd", "amount_usd"))
            price = _float(_first(a, "price_from_in_usd", "price_to_in_usd", "price_usd"))
            trader = _first(a, "tx_from_address", "trader_address", "maker_address", "user_address")
            tx_hash = _first(a, "tx_hash", "transaction_hash")
            timestamp = _int(_first(a, "block_timestamp", "timestamp"))
            result.append(TradeObservation(timestamp, side, volume, price, trader, tx_hash, row))
        return result
