from statistics import mean, pstdev
from .models import Trade


def summarize(trades: list[Trade], capital_per_trade: float = 0.01) -> dict:
    pnls = [t.net_pnl_usd for t in trades]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p <= 0]
    gross_returns = [t.gross_return_pct for t in trades]
    return {
        "trades": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": len(wins) / len(trades) if trades else 0.0,
        "total_pnl_usd": sum(pnls),
        "avg_pnl_usd": mean(pnls) if pnls else 0.0,
        "max_pnl_usd": max(pnls) if pnls else 0.0,
        "min_pnl_usd": min(pnls) if pnls else 0.0,
        "avg_gross_return_pct": mean(gross_returns) if gross_returns else 0.0,
        "pnl_stddev_usd": pstdev(pnls) if len(pnls) > 1 else 0.0,
        "capital_per_trade_usd": capital_per_trade,
    }
