from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class DiscoveredPool:
    source: str
    network: str
    pool_address: str | None
    base_token_address: str | None
    base_token_symbol: str | None
    base_token_name: str | None
    quote_token_address: str | None
    quote_token_symbol: str | None
    quote_token_name: str | None
    dex_id: str | None
    pool_created_at: datetime | None
    price_usd: float | None
    liquidity_usd: float | None
    fdv_usd: float | None
    volume_24h_usd: float | None
    discovered_at: datetime
    source_payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        for key, item in value.items():
            if isinstance(item, datetime):
                value[key] = item.isoformat()
        return value
