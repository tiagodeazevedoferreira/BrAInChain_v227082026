from dataclasses import dataclass


@dataclass(frozen=True)
class ExitConfig:
    trailing_stop_pct: float = 20.0
    take_profit_pct: float = 100.0
    reversal_score_threshold: float = 70.0
    liquidity_floor_usd: float = 100.0
    max_hold_minutes: int = 1440


@dataclass(frozen=True)
class PositionSnapshot:
    token_id: str
    entry_price: float
    current_price: float
    peak_price: float
    entry_timestamp: str
    current_timestamp: str
    liquidity_usd: float
    momentum_score: float
    volume_reversal_score: float
    sell_pressure_score: float
    whale_exit_score: float
    crash_risk_score: float


@dataclass(frozen=True)
class ExitDecision:
    should_exit: bool
    reason: str
    exit_score: float
    peak_capture_pct: float
