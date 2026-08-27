# Architecture — Autonomous Crypto Launch Intelligence & Trading

## Architectural principle

Event-driven, modular, adapter-based architecture. Data ingestion, intelligence, dataset/ML, decisioning, paper execution and future live execution remain separable.

## Current implementation status

- Discovery: `crypto_discovery/` — implemented and validated.
- Security: `crypto_security/` — implemented and operationally validated.
- Market/on-chain: `crypto_market/` — implemented with bounded current-state persistence.
- Dataset/ML foundation: `crypto_ml/` — implemented and CI validated.
- Backtesting: `crypto_backtest/` — implemented and CI validated.
- Paper trading: `crypto_paper/` — implemented; operational CI validation pending.
- Firebase: operational state only; never an unbounded historical ML/trading store.
- Live execution: intentionally not implemented or enabled.

## Logical pipeline

```text
Blockchain / DEX
      |
      v
Discovery -> Normalization
      |
      +------> Security ------> HARD GATE
      |
      v
Market / On-chain Intelligence
      |
      v
Historical Snapshot Store (outside Firebase)
      |
      +------> Forward Labels
      |
      v
Features -> ML -> Validation
      |
      v
Opportunity + Risk Decision
      |
      +--> DO_NOT_TRADE
      |
      +--> Backtest
      |
      v
Paper Executor
      |
      +--> Position Ledger
      +--> PnL / Monitoring
      +--> Circuit Breakers
      |
      v
Exit Intelligence
      |
      v
Trade Outcomes
      |
      v
Learning / MLOps
      |
      v
[future] Restricted Live Execution
```

## Phase 6 — Paper Trading

`crypto_paper/` is simulation-only and deliberately contains no wallet signer, RPC transaction sender, DEX router or exchange credentials.

Implemented components:

- `PaperSignal` contract;
- configurable US$0.01 target position;
- simulated buy fill with fee and slippage;
- simulated close with fee and slippage;
- position ledger outside Firebase;
- realized and unrealized PnL;
- max-open-position and max-exposure gates;
- daily-loss circuit breaker;
- consecutive-loss circuit breaker;
- security gate precedence;
- liquidity and opportunity-score gates;
- operational event logging;
- monitoring snapshot;
- unit tests and GitHub Actions.

## Safety boundaries

- Paper mode is the only supported execution mode in Phase 6.
- A `DO_NOT_TRADE` security state cannot be overridden by opportunity score.
- Position target is an experiment, not a promise that a venue can execute US$0.01.
- Insufficient cash, liquidity, exposure or circuit-breaker conditions reject the signal.
- Firebase receives no unbounded paper-trade history.
- Live execution requires a later explicit authorization gate and is not part of Phase 6.

## ML and backtesting safety

- Future observations create labels but never decision-time features.
- Historical data remains outside Firebase.
- Production model promotion requires temporal validation, out-of-sample evidence, calibration, stability and economic backtesting.
- Paper results are evidence, not proof of future profitability.

## Security boundaries

Private keys and signing material must never be stored in source code, normal logs or unencrypted configuration. Live execution must have explicit owner authorization, independent risk gates and circuit breakers.

## Failure philosophy

The default for stale data, uncertain contract state, abnormal liquidity, excessive slippage, provider instability, execution uncertainty or security uncertainty is `DO_NOT_TRADE`.
