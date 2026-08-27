from abc import ABC, abstractmethod
from datetime import datetime, timezone

import requests

from .models import DiscoveredPool


class DiscoveryAdapter(ABC):
    source: str

    @abstractmethod
    def discover(self) -> list[DiscoveredPool]:
        raise NotImplementedError


def _float(value):
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _datetime(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


class GeckoTerminalAdapter(DiscoveryAdapter):
    """Discovers recently created pools across GeckoTerminal-supported networks."""

    source = "geckoterminal"
    base_url = "https://api.geckoterminal.com/api/v2"

    def __init__(self, session=None, pages: int = 1, timeout: int = 20):
        self.session = session or requests.Session()
        self.pages = max(1, pages)
        self.timeout = timeout

    def discover(self) -> list[DiscoveredPool]:
        discovered = []
        for page in range(1, self.pages + 1):
            response = self.session.get(
                f"{self.base_url}/networks/new_pools",
                params={"include": "base_token,quote_token,dex", "page": page},
                headers={"Accept": "application/json;version=20230203"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            body = response.json()
            included = body.get("included", [])

            for item in body.get("data", []):
                attributes = item.get("attributes", {})
                relationships = item.get("relationships", {})
                base_id = (relationships.get("base_token", {}).get("data") or {}).get("id")
                quote_id = (relationships.get("quote_token", {}).get("data") or {}).get("id")
                base = next((x.get("attributes", {}) for x in included if x.get("id") == base_id), {})
                quote = next((x.get("attributes", {}) for x in included if x.get("id") == quote_id), {})
                dex_id = (relationships.get("dex", {}).get("data") or {}).get("id")
                network = item.get("id", "unknown").split("_", 1)[0]

                discovered.append(
                    DiscoveredPool(
                        source=self.source,
                        network=network,
                        pool_address=attributes.get("address"),
                        base_token_address=base.get("address"),
                        base_token_symbol=base.get("symbol"),
                        base_token_name=base.get("name"),
                        quote_token_address=quote.get("address"),
                        quote_token_symbol=quote.get("symbol"),
                        quote_token_name=quote.get("name"),
                        dex_id=dex_id,
                        pool_created_at=_datetime(attributes.get("pool_created_at")),
                        price_usd=_float(attributes.get("base_token_price_usd")),
                        liquidity_usd=_float(attributes.get("reserve_in_usd")),
                        fdv_usd=_float(attributes.get("fdv_usd")),
                        volume_24h_usd=_float(attributes.get("volume_usd", {}).get("h24")),
                        discovered_at=datetime.now(timezone.utc),
                        source_payload=item,
                    )
                )
        return discovered


class DexScreenerAdapter(DiscoveryAdapter):
    """Uses DEX Screener's latest token profiles and pair lookup as a second discovery signal."""

    source = "dexscreener"
    base_url = "https://api.dexscreener.com"

    def __init__(self, session=None, timeout: int = 20):
        self.session = session or requests.Session()
        self.timeout = timeout

    def discover(self) -> list[DiscoveredPool]:
        response = self.session.get(f"{self.base_url}/token-profiles/latest/v1", timeout=self.timeout)
        response.raise_for_status()
        profiles = response.json()
        discovered = []
        now = datetime.now(timezone.utc)

        for profile in profiles:
            chain = profile.get("chainId")
            token = profile.get("tokenAddress")
            if not chain or not token:
                continue

            try:
                pairs_response = self.session.get(
                    f"{self.base_url}/tokens/v1/{chain}/{token}", timeout=self.timeout
                )
                pairs_response.raise_for_status()
                pairs = pairs_response.json()
            except requests.RequestException:
                continue

            for pair in pairs:
                created_at = None
                if pair.get("pairCreatedAt"):
                    try:
                        created_at = datetime.fromtimestamp(
                            pair["pairCreatedAt"] / 1000, tz=timezone.utc
                        )
                    except (TypeError, ValueError, OSError):
                        pass

                discovered.append(
                    DiscoveredPool(
                        source=self.source,
                        network=chain,
                        pool_address=pair.get("pairAddress"),
                        base_token_address=token,
                        base_token_symbol=pair.get("baseToken", {}).get("symbol"),
                        base_token_name=pair.get("baseToken", {}).get("name"),
                        quote_token_address=pair.get("quoteToken", {}).get("address"),
                        quote_token_symbol=pair.get("quoteToken", {}).get("symbol"),
                        quote_token_name=pair.get("quoteToken", {}).get("name"),
                        dex_id=pair.get("dexId"),
                        pool_created_at=created_at,
                        price_usd=_float(pair.get("priceUsd")),
                        liquidity_usd=_float(pair.get("liquidity", {}).get("usd")),
                        fdv_usd=_float(pair.get("fdv")),
                        volume_24h_usd=_float(pair.get("volume", {}).get("h24")),
                        discovered_at=now,
                        source_payload=pair,
                    )
                )
        return discovered


class CompositeDiscovery:
    """Combines adapters, deduplicates observations and isolates source failures."""

    def __init__(self, adapters):
        self.adapters = adapters

    def discover(self) -> tuple[list[DiscoveredPool], list[dict]]:
        merged = {}
        errors = []
        for adapter in self.adapters:
            try:
                for item in adapter.discover():
                    key = (
                        item.network.lower(),
                        (item.base_token_address or "").lower(),
                        (item.pool_address or "").lower(),
                    )
                    merged[key] = item
            except Exception as exc:
                errors.append({"source": adapter.source, "error": str(exc)})
        return list(merged.values()), errors
