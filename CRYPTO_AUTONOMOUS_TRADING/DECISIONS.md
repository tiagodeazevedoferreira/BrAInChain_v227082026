# Decisions — Autonomous Crypto Launch Intelligence & Trading

## D-001 — Trading starts in paper mode
**Decision:** The system must start with `TRADING_MODE=paper`.

## D-002 — Security gates opportunity
**Decision:** Security and market-integrity checks have precedence over ML opportunity scores. A high ML score cannot override critical risk.

## D-003 — US$0.01 is an initial experimental target
**Decision:** Use a configurable initial position target of US$0.01. Venue minimums, gas, fees and slippage may make it uneconomic.

## D-004 — Peak is a probabilistic reversal problem
**Decision:** Do not assume the exact market peak can be known in real time. Use trailing stops, dynamic exits and reversal signals.

## D-005 — Time-series validation
**Decision:** ML validation must respect temporal ordering and avoid leakage/survivorship bias.

## D-006 — Modular adapters
**Decision:** Blockchain, DEX, data-provider and execution integrations use adapters.

## D-007 — Fail safe
**Decision:** Critical missing/uncertain information results in `DO_NOT_TRADE`.

## D-008 — Explicit live-trading gate
**Decision:** Live trading requires explicit configuration, validation evidence, risk limits and owner authorization.

Minimum conceptual gates:
- `TRADING_MODE=live`
- `LIVE_TRADING_ENABLED=true`
- risk limits configured
- security tests passed
- backtesting/out-of-sample/paper evidence available
- explicit owner authorization

## D-009 — Auditability
Every model and trade decision must be reproducible from timestamped features, model version, scores, decision and outcome.

## D-010 — No blind auto-learning in production
Production models cannot silently retrain and replace themselves.

## D-011 — Inspect existing architecture first
Do not assume a proposed stack or directory structure is compatible with the current repository.

## D-012 — Security provider evidence is advisory
Honeypot.is/GoPlus evidence is not a formal smart-contract audit. Local deterministic gates remain authoritative.

## D-013 — Security analysis is incremental
Only unprocessed discovery tokens should consume expensive security-provider capacity where possible.

## D-014 — Liquidity lock is never inferred
Unknown lock status remains unknown and contributes risk.

## D-015 — Firebase is operational state, not a historical data lake
Historical ML/backtesting/trade data must use dedicated storage with retention and growth controls.

## D-016 — Market intelligence does not invent unavailable data
Missing holder-growth, wallet-history or provider fields remain `unknown`/`null` and never become positive evidence.

## D-017 — Smart-money score is initially a proxy
Until wallet-history evidence exists, smart-money scoring is explicitly a behavioral proxy.

## D-018 — Live transport is independently fail-closed
**Decision:** Phase 8 may create the safety boundary for live execution, but no venue adapter or real order transport is enabled automatically.

**Rule:** Even when `TRADING_MODE=live`, `LIVE_TRADING_ENABLED=true` and preflight is configured, the executor must return `BLOCKED` until a separately reviewed/approved venue adapter exists and all empirical evidence and owner authorization gates are satisfied.

**Reason:** A configuration error must never be capable of turning development or CI into an unintended real-money transaction.
