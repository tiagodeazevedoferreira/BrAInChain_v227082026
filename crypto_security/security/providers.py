from __future__ import annotations

import os
from typing import Any

import requests


CHAIN_IDS = {
    "eth": 1, "ethereum": 1, "bsc": 56, "polygon_pos": 137, "polygon": 137,
    "arbitrum": 42161, "avalanche": 43114, "base": 8453, "optimism": 10,
    "fantom": 250, "linea": 59144, "cronos": 25, "gnosis": 100,
    "mantle": 5000, "zksync-era": 324, "zksync": 324, "opbnb": 204,
    "blast": 81457, "scroll": 534352, "monad": 143, "plasma": 9745,
    "sonic": 146, "unichain": 130, "world-chain": 480, "soneium": 1868,
}


def chain_id(network: str) -> int | None:
    key = (network or "").lower().replace(" ", "-")
    if key.isdigit():
        return int(key)
    return CHAIN_IDS.get(key)


class HoneypotProvider:
    name = "honeypot_is"
    base_url = "https://api.honeypot.is"

    def __init__(self, session: requests.Session | None = None, timeout: int = 20):
        self.session = session or requests.Session()
        self.timeout = timeout
        self.api_key = os.getenv("HONEYPOT_API_KEY")

    def _headers(self) -> dict[str, str]:
        return {"X-API-KEY": self.api_key} if self.api_key else {}

    def check(self, address: str, network: str, pair: str | None = None) -> dict[str, Any]:
        cid = chain_id(network)
        params: dict[str, Any] = {"address": address}
        if cid is not None:
            params["chainID"] = cid
        if pair:
            params["pair"] = pair
        response = self.session.get(
            f"{self.base_url}/v2/IsHoneypot",
            params=params,
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def top_holders(self, address: str, network: str) -> dict[str, Any]:
        cid = chain_id(network)
        if cid is None:
            raise ValueError(f"Unsupported chain for top holders: {network}")
        response = self.session.get(
            f"{self.base_url}/v1/TopHolders",
            params={"address": address, "chainID": cid},
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def contract_verification(self, address: str, network: str) -> dict[str, Any]:
        params: dict[str, Any] = {"address": address}
        cid = chain_id(network)
        if cid is not None:
            params["chainID"] = cid
        response = self.session.get(
            f"{self.base_url}/v2/GetContractVerification",
            params=params,
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()


class GoPlusProvider:
    name = "goplus"
    base_url = "https://api.gopluslabs.io/api/v1"

    def __init__(self, session: requests.Session | None = None, timeout: int = 20):
        self.session = session or requests.Session()
        self.timeout = timeout
        self.access_token = os.getenv("GOPLUS_ACCESS_TOKEN")

    @property
    def enabled(self) -> bool:
        return bool(self.access_token)

    def token_security(self, address: str, network: str) -> dict[str, Any]:
        cid = chain_id(network)
        if cid is None:
            raise ValueError(f"Unsupported chain for GoPlus: {network}")
        if not self.access_token:
            raise RuntimeError("GOPLUS_ACCESS_TOKEN is not configured")
        response = self.session.get(
            f"{self.base_url}/token_security/{cid}",
            params={"contract_addresses": address},
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        body = response.json()
        return body.get("result", {}).get(address.lower(), body.get("result", {}))
