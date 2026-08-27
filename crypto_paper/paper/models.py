from dataclasses import dataclass, field


@dataclass(frozen=True)
class PaperSignal:
    timestamp: str
    token_id: str
    price_usd: float
    liquidity_usd: float
    opportunity_score: float
    security_gate: str
    signal: str
    model_version: str = "research"


@dataclass
class PaperPosition:
    position_id: str
    token_id: str
    opened_at: str
    entry_price_usd: float
    quantity: float
    invested_usd: float
    fees_usd: float
    status: str = "OPEN"
    exit_price_usd: float | None = None
    closed_at: str | None = None
    realized_pnl_usd: float | None = None
    exit_reason: str | None = None
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class PaperConfig:
    initial_capital_usd: float = 100.0
    position_target_usd: float = 0.01
    fee_bps: float = 30.0
    slippage_bps: float = 100.0
    max_open_positions: int = 100
    max_exposure_usd: float = 1.0
    daily_loss_limit_usd: float = 0.50
    max_consecutive_losses: int = 5
    min_liquidity_usd: float = 100.0
    min_opportunity_score: float = 70.0


@dataclass(frozen=True)
class PaperAccount:
    cash_usd: float
    equity_usd: float
    realized_pnl_usd: float
    open_positions: int
    halted: bool
    halt_reason: str | None = None
