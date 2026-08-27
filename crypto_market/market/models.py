from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class MarketObservation:
    network: str
    token_address: str
    pool_address: str
    dex_id: str | None
    symbol: str | None
    observed_at: str = field(default_factory=_now)
    price_usd: float | None = None
    liquidity_usd: float | None = None
    volume_1h_usd: float | None = None
    volume_6h_usd: float | None = None
    volume_24h_usd: float | None = None
    buys_1h: int | None = None
    sells_1h: int | None = None
    buys_6h: int | None = None
    sells_6h: int | None = None
    buys_24h: int | None = None
    sells_24h: int | None = None
    price_change_5m_pct: float | None = None
    price_change_1h_pct: float | None = None
    price_change_6h_pct: float | None = None
    price_change_24h_pct: float | None = None
    fdv_usd: float | None = None
    market_cap_usd: float | None = None
    boosts_active: int | None = None
    raw_source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TradeObservation:
    timestamp: int | None
    side: str | None
    volume_usd: float | None
    price_usd: float | None
    trader_address: str | None
    transaction_hash: str | None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IntelligenceAnalysis:
    network: str
    token_address: str
    pool_address: str
    analyzed_at: str
    market_score: float
    momentum_score: float
    liquidity_score: float
    pressure_score: float
    whale_score: float
    smart_money_proxy_score: float
    manipulation_risk_score: float
    holder_growth_score: float | None
    unique_traders_24h: int | None
    buy_volume_24h_usd: float | None
    sell_volume_24h_usd: float | None
    decision: str
    flags: list[str]
    features: dict[str, float | int | None]
    provider_status: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
