from dataclasses import dataclass


@dataclass(frozen=True)
class MarketEvent:
    timestamp: str
    token_id: str
    price_usd: float
    liquidity_usd: float
    signal_score: float
    security_passed: bool


@dataclass(frozen=True)
class BacktestConfig:
    capital_usd: float = 0.01
    fee_bps: float = 30.0
    slippage_bps: float = 100.0
    gas_usd: float = 0.0
    min_liquidity_usd: float = 100.0
    min_score: float = 70.0


@dataclass(frozen=True)
class Trade:
    token_id: str
    entry_timestamp: str
    exit_timestamp: str
    gross_return_pct: float
    net_pnl_usd: float
    reason: str
