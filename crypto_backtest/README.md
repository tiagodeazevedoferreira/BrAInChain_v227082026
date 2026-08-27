# Crypto Backtesting Engine

Phase 5 provides a deterministic, leakage-safe event-driven backtesting foundation for the autonomous trading system.

## Principles

- historical data is not stored in Firebase;
- decisions use only information available at the event timestamp;
- fees, slippage, gas and execution constraints are explicit;
- security failures can block entries;
- every trade is journaled;
- the engine never executes live orders.

The engine is intentionally conservative: if an execution assumption is missing, the trade is rejected rather than silently making an optimistic assumption.
