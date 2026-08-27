# Architecture — Autonomous Crypto Launch Intelligence & Trading

## Architectural principle

Event-driven, modular, adapter-based architecture. Data ingestion, intelligence, ML, decisioning and execution remain separable.

## Current implementation status

- Discovery layer: implemented in `crypto_discovery/`.
- Security layer: implemented in `crypto_security/` and validated operationally.
- Market/on-chain intelligence: implemented in `crypto_market/` with current-state persistence and provider failure isolation.
- Firebase persistence: operational state only; no unbounded historical snapshots.
- GitHub Actions: discovery, security and market-intelligence automation.
- ML/execution: not implemented yet.

## Logical pipeline

```text
Blockchain / DEX / Social Sources
            |
            v
      Discovery Layer
            |
            v
      Normalization
            |
            +----------------+
            |                |
            v                v
      Security        Market/On-chain Intelligence
                         |   |   |   |
                         |   |   |   +-- Wallet activity
                         |   |   +------ Trade pressure
                         |   +---------- Market metrics
                         +-------------- Liquidity/momentum
            |
            v
     Feature Engineering
            |
            v
       ML Ensemble
            |
            +----------------+
            |                |
            v                v
   Opportunity Score    Risk Score
            \                /
             \              /
              v            v
              Decision Engine
                    |
             +------+------+
             |             |
             v             v
           Paper          Live
          Executor      Executor
             |             |
             +------+------+
                    |
                    v
             Position Monitor
                    |
                    v
                Exit Engine
                    |
                    v
              Trade Outcomes
                    |
                    v
             Learning / MLOps
```

## Implemented Phase 3 — Market & On-chain Intelligence

`crypto_market/` contains:

- `MarketObservation` and `TradeObservation` normalized models;
- DEX Screener market adapter using documented pair endpoints;
- GeckoTerminal trade adapter using documented pool-trade endpoints;
- price, volume, liquidity and transaction metrics;
- buy/sell pressure;
- momentum and price-acceleration proxies;
- liquidity turnover;
- unique trader/wallet activity when provider data exposes trader addresses;
- largest-trade concentration / whale-risk proxy;
- net-buy / smart-money proxy;
- pump/manipulation heuristics;
- fail-closed provider handling;
- bounded Firebase sink storing only latest market state;
- unit and engine tests;
- GitHub Actions workflow every 10 minutes plus manual dispatch.

### Explicit data gaps

- Holder growth requires two observations of holder count. The current security layer has a point-in-time holder count, but Firebase is intentionally not used as a historical data lake. A bounded baseline or external historical dataset will be introduced with the dataset phase.
- Smart-money score is currently a proxy from trade behavior, not a claim of wallet profitability. Historical wallet performance will require a dedicated dataset.
- Whale detection is currently trade-concentration based, not full holder concentration analytics; security provides complementary holder concentration.

## Implemented Security Intelligence

`crypto_security/` contains:

- `SecurityAnalysis` audit model;
- `HoneypotProvider`;
- `GoPlusProvider` optional adapter;
- contract verification;
- honeypot/simulation analysis;
- buy/sell/transfer tax analysis;
- holder sell-failure/siphoning analysis;
- top-holder/top-5 concentration;
- source/proxy analysis;
- deterministic risk scoring;
- hard `DO_NOT_TRADE` security gate;
- Firebase sink;
- incremental Firebase runner;
- unit/integration tests.

Security data is stored under `security/tokens/*` and aggregate run state under `security/status`.

## Proposed components

### Discovery
- TokenDiscoveryEngine
- DexDiscoveryEngine
- BlockchainAdapter
- DexAdapter

### Intelligence
- TokenSecurityEngine
- OnChainAnalyticsEngine
- SmartMoneyEngine
- MarketMicrostructureEngine
- SocialSentimentEngine
- PumpDetectionEngine

### ML
- FeatureEngineeringEngine
- MLPredictionEngine
- ExtremeOpportunityDetector
- ModelRegistry
- Training/validation pipeline

### Decision and risk
- OpportunityScoreEngine
- RiskScoreEngine
- TradingDecisionEngine
- CircuitBreaker

### Execution
- TradeExecutionEngine
- DEXExecutor
- CEXExecutor
- SecureSigner
- PaperExecutor

### Portfolio
- PositionManager
- PnLCalculator
- ExposureManager

### Exit
- PositionExitEngine
- PeakDetectionEngine

### Operations
- Notification adapters
- Logging
- Metrics
- Health checks
- Audit trail

## Data model

Core entities:

- Token
- Pool
- LiquidityEvent
- PriceSnapshot
- VolumeSnapshot
- HolderSnapshot
- Wallet
- WalletEvent
- SecurityAnalysis
- MarketObservation
- TradeObservation
- SocialMetric
- MLPrediction
- Signal
- Position
- Trade
- Exit
- ModelVersion
- BacktestRun
- SystemEvent

## Storage policy

Firebase Realtime Database is an operational state store, not the historical ML data lake. Discovery, security and market modules write current state plus bounded aggregate status. They must not append unbounded per-run snapshots to RTDB.

Historical observations required for ML/backtesting must use a dedicated dataset storage strategy with explicit retention, partitioning, size monitoring and migration/archival controls.

## Security boundaries

Private keys and signing material must never be stored in source code, normal logs or unencrypted configuration. Execution must occur behind a secure signer abstraction.

Live execution must have an explicit feature flag and independent risk gates.

Security providers are evidence sources, not an absolute guarantee. Unknown or contradictory critical security state must result in `DO_NOT_TRADE`.

## Failure philosophy

The default behavior for stale data, uncertain contract state, abnormal liquidity, excessive slippage, RPC/API instability, execution uncertainty or security uncertainty is `DO_NOT_TRADE`.

## Technology candidates

Backend: Python, FastAPI, Pydantic, SQLAlchemy.

Data: PostgreSQL, Redis, Polars/Pandas, partitioned Parquet/object storage/DuckDB for historical datasets.

ML: LightGBM/XGBoost, PyTorch.

Execution/data transport: async I/O, WebSockets where supported.

Frontend: React/Next.js/TypeScript.

Deployment: Docker and GitHub Actions.

These are candidate technologies, not immutable requirements; the current repository is the source of truth for implementation decisions.
