from .models import PaperConfig, PaperPosition


class PaperRiskManager:
    def __init__(self, config: PaperConfig):
        self.config = config
        self.halted = False
        self.halt_reason = None
        self.consecutive_losses = 0

    def can_open(self, positions: list[PaperPosition], exposure_usd: float) -> tuple[bool, str | None]:
        if self.halted:
            return False, self.halt_reason or "CIRCUIT_BREAKER"
        if len([p for p in positions if p.status == "OPEN"]) >= self.config.max_open_positions:
            return False, "MAX_OPEN_POSITIONS"
        if exposure_usd + self.config.position_target_usd > self.config.max_exposure_usd:
            return False, "MAX_EXPOSURE"
        if self.config.position_target_usd <= 0:
            return False, "INVALID_POSITION_SIZE"
        return True, None

    def record_result(self, pnl_usd: float, daily_pnl_usd: float) -> None:
        if pnl_usd < 0:
            self.consecutive_losses += 1
        elif pnl_usd > 0:
            self.consecutive_losses = 0
        if daily_pnl_usd <= -abs(self.config.daily_loss_limit_usd):
            self.halted = True
            self.halt_reason = "DAILY_LOSS_LIMIT"
        elif self.consecutive_losses >= self.config.max_consecutive_losses:
            self.halted = True
            self.halt_reason = "MAX_CONSECUTIVE_LOSSES"
