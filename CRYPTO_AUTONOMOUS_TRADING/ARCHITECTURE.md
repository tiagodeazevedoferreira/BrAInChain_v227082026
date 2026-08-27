# Architecture — Autonomous Crypto Launch Intelligence & Trading

## Architectural principle

Event-driven, modular, adapter-based architecture. Data ingestion, intelligence, dataset/ML, decisioning and execution remain separable.

## Current implementation status

- Discovery: `crypto_discovery/` — implemented and validated.
- Security: `crypto_security/` — implemented and operationally validated.
- Market/on-chain: `crypto_market/` — implemented with bounded current-state persistence.
- Dataset/ML foundation: `crypto_ml/` — implemented; production promotion remains gated on sufficient real history and temporal validation.
- Firebase: operational state only; never an unbounded historical ML store.
- Execution: intentionally not implemented/enabled.

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
      +------> Forward Labels (future only)
      |
      v
Time-aware Feature Engineering
      |
      v
Training / Validation / Walk-forward
      |
      v
ML Ensemble -> Opportunity + Risk
      |
      v
Decision Engine
      |
      +--> DO_NOT_TRADE
      |
      +--> Paper / later restricted Live
                  |
                  v
             Position Monitor
                  |
                  v
             Exit Intelligence
                  |
                  v
             Trade Outcomes
                  |
                  v
             Learning / MLOps
```

## Implemented Phase 4 — Dataset & ML Foundation

`crypto_ml/` contains:

- normalized `Snapshot` contract for historical observations;
- append-only JSONL storage abstraction outside Firebase;
- multi-horizon forward labels at 1h/6h/24h/72h;
- growth thresholds +10/+25/+50/+100/+500/+1000%;
- severe collapse/rug class;
- `UNKNOWN` labels when future data does not exist;
- time-aware feature extraction from decision-time data only;
- readiness gate for observations, unique tokens and labeled samples;
- balanced Random Forest baseline;
- unit tests and GitHub Actions.

The baseline is a research baseline, not a production trading model.

## Data/ML safety rules

- Future observations may be used to create labels but never to create decision-time features.
- Missing future observations must not silently become negative labels.
- A model cannot be promoted based only on accuracy.
- Production promotion requires time-aware splits, walk-forward evaluation, out-of-sample results, calibration, stability and economic backtesting.
- Historical snapshots must not be appended indefinitely to Firebase.

## Storage policy

Firebase Realtime Database is an operational state store. Discovery, security and market modules write current state and bounded aggregate status. Historical ML/backtest observations use a dedicated storage abstraction with explicit retention and partitioning. The initial implementation is portable JSONL; migration to Parquet/object storage/DuckDB is intentionally isolated behind the storage contract.

## Proposed next components

### Intelligence
- OnChainAnalyticsEngine
- SmartMoneyEngine
- MarketMicrostructureEngine
- SocialSentimentEngine
- PumpDetectionEngine

### ML
- FeatureEngineeringEngine
- ExtremeOpportunityDetector
- ensemble comparison
- calibration
- walk-forward evaluator
- model registry/versioning

### Backtesting/execution
- EventDrivenBacktester
- PaperExecutor
- DEXExecutor/CEXExecutor
- SecureSigner
- PositionManager
- ExitEngine

## Security boundaries

Private keys and signing material must never be stored in source code, normal logs or unencrypted configuration. Live execution must have explicit owner authorization, independent risk gates and circuit breakers.

## Failure philosophy

The default for stale data, uncertain contract state, abnormal liquidity, excessive slippage, provider instability, execution uncertainty or security uncertainty is `DO_NOT_TRADE`.
