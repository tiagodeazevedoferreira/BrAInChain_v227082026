from dataclasses import dataclass


@dataclass(frozen=True)
class LiveConfig:
    trading_mode: str = "paper"
    live_trading_enabled: bool = False
    owner_authorized: bool = False
    position_target_usd: float = 0.01
    max_exposure_usd: float = 0.10
    max_open_positions: int = 1
    max_gas_usd: float = 0.01
    max_slippage_bps: float = 300.0
    max_daily_loss_usd: float = 0.02
    max_consecutive_losses: int = 2

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.trading_mode != "live":
            errors.append("TRADING_MODE_MUST_BE_LIVE")
        if not self.live_trading_enabled:
            errors.append("LIVE_TRADING_DISABLED")
        if not self.owner_authorized:
            errors.append("OWNER_AUTHORIZATION_REQUIRED")
        if self.position_target_usd <= 0:
            errors.append("INVALID_POSITION_SIZE")
        if self.max_exposure_usd < self.position_target_usd:
            errors.append("EXPOSURE_LIMIT_BELOW_POSITION_SIZE")
        if self.max_open_positions < 1:
            errors.append("INVALID_MAX_OPEN_POSITIONS")
        if self.max_gas_usd < 0 or self.max_slippage_bps < 0:
            errors.append("INVALID_EXECUTION_LIMIT")
        if self.max_daily_loss_usd <= 0 or self.max_consecutive_losses < 1:
            errors.append("INVALID_CIRCUIT_BREAKER")
        return errors
