# Decisions — Autonomous Crypto Launch Intelligence & Trading

## D-001 — Trading starts in paper mode

**Decision:** The system must start with `TRADING_MODE=paper`.

**Reason:** Real-money execution must not be used to validate the architecture or ML hypotheses.

## D-002 — Security gates opportunity

**Decision:** Security and market-integrity checks have precedence over ML opportunity scores.

**Rule:** A high ML score cannot override a critical contract, honeypot, rug-pull or liquidity risk.

## D-003 — US$0.01 is an initial experimental target, not a guaranteed executable amount

**Decision:** Use a configurable initial position target of US$0.01.

**Reason:** Real venues may impose minimum order sizes and transaction costs can exceed the intended position. The system must skip economically invalid trades rather than bypass platform rules.

## D-004 — Peak is treated as a probabilistic reversal problem

**Decision:** Do not assume the exact market peak can be known in real time.

**Implementation direction:** trailing stops, dynamic exits, momentum/volume reversal, whale selling, liquidity deterioration and probabilistic peak detection.

## D-005 — Time-series validation

**Decision:** ML validation must respect temporal ordering.

**Required:** walk-forward validation, time-series cross-validation and out-of-sample testing where appropriate. Avoid future-data leakage and survivorship bias.

## D-006 — Modular adapters

**Decision:** Blockchain, DEX, data-provider and execution integrations must use adapters.

**Reason:** Providers and networks change; the intelligence core should not depend directly on a single provider.

## D-007 — Fail safe

**Decision:** When critical information is unavailable or uncertain, the system must not trade.

Examples: stale price, unknown contract, excessive slippage, abnormal liquidity, RPC instability, execution uncertainty or security uncertainty.

## D-008 — Explicit live-trading gate

**Decision:** Live trading requires an explicit configuration separate from the general trading mode.

Minimum conceptual gates:
- `TRADING_MODE=live`
- `LIVE_TRADING_ENABLED=true`
- risk limits configured
- security tests passed
- backtesting/out-of-sample/paper evidence available
- explicit owner authorization

## D-009 — Auditability

Every model decision and trade decision must be reproducible from timestamped features, model version, risk score, opportunity score, decision and outcome.

## D-010 — No blind auto-learning in production

**Decision:** Production models cannot silently retrain and replace themselves.

Training → validation → backtest → approval → deployment → monitoring → rollback must be explicit and versioned.

## D-011 — Existing BrAInChain architecture must be inspected before implementation

**Decision:** Do not assume the proposed technology stack or directory structure is compatible with the current repository. First inspect the repository and reuse existing infrastructure whenever appropriate.
