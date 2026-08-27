from .models import BacktestConfig, MarketEvent, Trade


def _execution_factor(config: BacktestConfig) -> float:
    return 1.0 - (config.fee_bps + config.slippage_bps) / 10_000.0


def run(events: list[MarketEvent], config: BacktestConfig | None = None) -> list[Trade]:
    config = config or BacktestConfig()
    if config.capital_usd <= 0:
        raise ValueError("capital_usd must be positive")
    if not 0 <= config.fee_bps + config.slippage_bps < 10_000:
        raise ValueError("fee + slippage must be between 0 and 10000 bps")

    trades: list[Trade] = []
    open_event: MarketEvent | None = None
    for event in sorted(events, key=lambda x: x.timestamp):
        if open_event is None:
            if event.security_passed and event.liquidity_usd >= config.min_liquidity_usd and event.signal_score >= config.min_score:
                open_event = event
            continue

        if event.token_id != open_event.token_id:
            continue
        if event.price_usd <= 0 or open_event.price_usd <= 0:
            continue

        gross = event.price_usd / open_event.price_usd - 1.0
        net_factor = _execution_factor(config)
        net_value = config.capital_usd * (1.0 + gross) * net_factor - config.gas_usd
        pnl = net_value - config.capital_usd
        trades.append(Trade(open_event.token_id, open_event.timestamp, event.timestamp, gross * 100.0, pnl, "next_observation"))
        open_event = None
    return trades
