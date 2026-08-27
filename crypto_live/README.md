# Phase 8 — Restricted Live Micro Trading

This phase creates the safety boundary for a future live execution adapter. It does **not** enable or submit real orders.

## Gates

Live operation requires all of the following:

- `TRADING_MODE=live`;
- `LIVE_TRADING_ENABLED=true`;
- explicit owner authorization;
- satisfactory backtest evidence;
- out-of-sample evidence;
- paper-trading evidence;
- security tests;
- failure-mode tests;
- secure signing/secret configuration;
- configured exposure, position, gas, slippage and loss limits.

The current `LiveExecutor` intentionally returns `BLOCKED` because no approved venue adapter exists yet. This prevents a configuration mistake from becoming a real-money transaction.

## Important validation distinction

Passing the Phase 8 CI only proves the safety boundary works. It does not prove the strategy is profitable or authorize live trading.

Before adding a venue adapter, the project must produce empirical out-of-sample and paper-trading evidence and complete a separate security/review gate.
