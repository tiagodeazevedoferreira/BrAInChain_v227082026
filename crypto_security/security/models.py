from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class SecurityAnalysis:
    network: str
    token_address: str
    pool_address: str | None
    symbol: str | None
    name: str | None
    analyzed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    provider_status: dict[str, str] = field(default_factory=dict)
    honeypot: bool | None = None
    honeypot_reason: str | None = None
    simulation_success: bool | None = None
    buy_tax_pct: float | None = None
    sell_tax_pct: float | None = None
    transfer_tax_pct: float | None = None
    open_source: bool | None = None
    root_open_source: bool | None = None
    is_proxy: bool | None = None
    has_proxy_calls: bool | None = None
    holder_count: int | None = None
    analyzed_holders: int | None = None
    holder_sell_failures: int | None = None
    holder_siphoned: int | None = None
    top_holder_pct: float | None = None
    top_5_holders_pct: float | None = None
    liquidity_usd: float | None = None
    liquidity_locked_pct: float | None = None
    liquidity_lock_known: bool = False
    risk_score: float = 100.0
    risk_level: str = "unknown"
    trade_gate: str = "DO_NOT_TRADE"
    critical_flags: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["analyzed_at"] = self.analyzed_at.isoformat()
        return value
