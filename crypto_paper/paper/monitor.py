from .models import PaperPosition


def snapshot(positions: list[PaperPosition], prices: dict[str, float]) -> dict:
    open_positions = [p for p in positions if p.status == "OPEN"]
    market_value = 0.0
    unrealized = 0.0
    for p in open_positions:
        price = prices.get(p.token_id)
        if price is None or price <= 0:
            continue
        value = p.quantity * price
        market_value += value
        unrealized += value - p.invested_usd
    return {"open_positions": len(open_positions), "market_value_usd": market_value, "unrealized_pnl_usd": unrealized}
