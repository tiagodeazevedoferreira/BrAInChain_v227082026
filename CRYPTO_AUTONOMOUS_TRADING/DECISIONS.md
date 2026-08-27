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

## D-012 — Security provider evidence is advisory, but the gate is deterministic

**Decision:** Security providers such as Honeypot.is and optional GoPlus are evidence sources. They do not constitute a formal smart-contract audit and must not be treated as infallible.

**Rule:** The local security engine combines provider evidence with deterministic hard gates. Unknown/unsupported critical security state results in `DO_NOT_TRADE` rather than an optimistic assumption.

## D-013 — Security analysis is incremental

**Decision:** The security runner processes only discovery tokens that do not yet have a security record.

**Reason:** Avoid repeatedly consuming provider capacity for unchanged tokens and allow newly discovered tokens to enter the security pipeline continuously.

## D-014 — Liquidity lock is never inferred

**Decision:** If no reliable evidence of a liquidity lock/locker is available, the state remains `unknown` and contributes risk. The engine never converts absence of evidence into proof of safety.

## D-015 — Firebase is operational state, not a historical data lake

**Decision:** Firebase RTDB may store current discovery/security/market state and bounded aggregate status, but not unbounded historical snapshots.

**Reason:** The previous project exhausted free RTDB capacity. Historical ML/backtesting data must use a dedicated, partitionable storage strategy with retention and growth controls.

## D-016 — Market intelligence does not invent unavailable data

**Decision:** Missing holder-growth, wallet-history or provider fields remain `unknown`/`null` and never become positive evidence.

**Reason:** A false positive in early-token intelligence can be more dangerous than an omitted signal.

## D-017 — Smart-money score is initially a proxy

**Decision:** Until a wallet-history dataset exists, smart-money scoring is explicitly a proxy based on observable trade behavior, not a claim that a wallet is profitable or historically predictive.
