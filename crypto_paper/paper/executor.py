from uuid import uuid4
from .models import PaperConfig, PaperPosition, PaperSignal
from .risk import PaperRiskManager


class PaperExecutor:
    """Simulates orders; it has no blockchain/CEX signing capability."""
    def __init__(self, config: PaperConfig, risk: PaperRiskManager | None = None):
        self.config = config
        self.risk = risk or PaperRiskManager(config)
        self.positions: dict[str, PaperPosition] = {}
        self.cash_usd = config.initial_capital_usd
        self.realized_pnl_usd = 0.0
        self.daily_pnl_usd = 0.0

    @property
    def exposure_usd(self) -> float:
        return sum(p.invested_usd for p in self.positions.values() if p.status == "OPEN")

    def process_signal(self, signal: PaperSignal) -> tuple[str, PaperPosition | None]:
        if signal.signal != "BUY":
            return "IGNORED_SIGNAL", None
        if signal.security_gate != "SECURITY_PASS":
            return "DO_NOT_TRADE_SECURITY_GATE", None
        if signal.price_usd <= 0 or signal.liquidity_usd < self.config.min_liquidity_usd:
            return "DO_NOT_TRADE_LIQUIDITY", None
        if signal.opportunity_score < self.config.min_opportunity_score:
            return "DO_NOT_TRADE_SCORE", None
        if self.cash_usd < self.config.position_target_usd:
            return "SKIPPED_INSUFFICIENT_CASH", None

        allowed, reason = self.risk.can_open(list(self.positions.values()), self.exposure_usd)
        if not allowed:
            return f"SKIPPED_{reason}", None

        effective_price = signal.price_usd * (1 + self.config.slippage_bps / 10_000)
        fee = self.config.position_target_usd * self.config.fee_bps / 10_000
        invested = self.config.position_target_usd - fee
        quantity = invested / effective_price
        position = PaperPosition(str(uuid4()), signal.token_id, signal.timestamp, effective_price, quantity, invested, fee, metadata={"model_version": signal.model_version})
        self.positions[position.position_id] = position
        self.cash_usd -= self.config.position_target_usd
        return "PAPER_BUY_FILLED", position

    def mark_to_market(self, position_id: str, timestamp: str, price_usd: float) -> float:
        p = self.positions[position_id]
        if p.status != "OPEN":
            raise ValueError("position is not open")
        if price_usd <= 0:
            raise ValueError("price_usd must be positive")
        return p.quantity * price_usd - p.invested_usd

    def close(self, position_id: str, timestamp: str, price_usd: float, reason: str = "MANUAL_PAPER_EXIT") -> PaperPosition:
        p = self.positions[position_id]
        if p.status != "OPEN":
            raise ValueError("position is not open")
        if price_usd <= 0:
            raise ValueError("price_usd must be positive")
        effective_price = price_usd * (1 - self.config.slippage_bps / 10_000)
        gross_value = p.quantity * effective_price
        exit_fee = gross_value * self.config.fee_bps / 10_000
        net_value = gross_value - exit_fee
        pnl = net_value - p.invested_usd - p.fees_usd
        p.exit_price_usd = effective_price
        p.closed_at = timestamp
        p.realized_pnl_usd = pnl
        p.status = "CLOSED"
        p.exit_reason = reason
        self.cash_usd += net_value
        self.realized_pnl_usd += pnl
        self.daily_pnl_usd += pnl
        self.risk.record_result(pnl, self.daily_pnl_usd)
        return p

    def account(self) -> dict:
        open_value = sum(p.quantity * p.entry_price_usd for p in self.positions.values() if p.status == "OPEN")
        return {"cash_usd": self.cash_usd, "equity_usd": self.cash_usd + open_value, "realized_pnl_usd": self.realized_pnl_usd, "open_positions": len([p for p in self.positions.values() if p.status == "OPEN"]), "halted": self.risk.halted, "halt_reason": self.risk.halt_reason}
