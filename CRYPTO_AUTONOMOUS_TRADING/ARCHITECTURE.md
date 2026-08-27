# Architecture — Autonomous Crypto Launch Intelligence & Trading

## Architectural principle

Event-driven, modular, adapter-based architecture. Discovery, security, market intelligence, dataset/ML, backtesting, paper execution, exit intelligence and future live execution remain separable.

## Current implementation status

- Discovery: `crypto_discovery/` — implemented and validated.
- Security: `crypto_security/` — implemented and validated.
- Market/on-chain: `crypto_market/` — implemented and validated.
- Dataset/ML: `crypto_ml/` — implemented and CI validated.
- Backtesting: `crypto_backtest/` — implemented and CI validated.
- Paper trading: `crypto_paper/` — implemented and CI validated.
- Exit intelligence: `crypto_exit/` — implemented and CI validated.
- Restricted live boundary: `crypto_live/` — implemented; CI validation pending.
- Firebase: operational state only; never an unbounded historical store.
- Actual live order transport: intentionally absent.

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
Restricted Live Safety Gate
      |
      +--> BLOCKED until evidence + authorization + approved venue adapter
      |
      v
[future] Approved Venue Adapter
      |
      v
Live Micro Execution
```

## Phase 8 — Restricted Live Safety Boundary

`crypto_live/` exists to prevent configuration mistakes from becoming real-money transactions.

Components:
- `LiveConfig`: explicit live mode, enablement, authorization and quantitative risk limits;
- `Evidence`: required validation evidence contract;
- `preflight`: independent fail-closed gate;
- `LiveExecutor`: safety boundary that currently rejects all real orders because no approved venue adapter exists;
- `.github/workflows/crypto-live.yml`: automated safety tests.

### Required gates

All must pass before a venue adapter can even be considered:

1. satisfactory empirical backtesting;
2. out-of-sample validation;
3. sustained paper-trading evidence;
4. security tests;
5. failure-mode tests;
6. secure signing/secret handling;
7. configured position/exposure/gas/slippage/loss limits;
8. explicit owner authorization;
9. separately reviewed venue adapter.

CI success is not profitability evidence and is not trading authorization.

## Storage

Firebase RTDB is restricted to current operational state and bounded aggregates. Historical ML, backtesting and trade-outcome data remain outside Firebase with retention and growth controls.

## Security boundaries

Private keys and signing material must never be stored in source code, normal logs or unencrypted configuration. The default on stale data, uncertain contract state, excessive slippage, abnormal liquidity, provider instability or execution uncertainty is `DO_NOT_TRADE`.

## ML/backtesting safety

Future observations may create labels but never decision-time features. Production promotion requires temporal validation, out-of-sample evidence, calibration, stability and economic backtesting. Paper results are evidence, not proof of future profitability.
