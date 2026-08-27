# Architecture — Autonomous Crypto Launch Intelligence & Trading

## Architectural principle

Event-driven, modular, adapter-based architecture. Data ingestion, intelligence, ML, decisioning and execution remain separable.

## Current implementation status

- Discovery layer: implemented in `crypto_discovery/`.
- Security layer: implemented in `crypto_security/`.
- Firebase persistence: implemented for discovery and security.
- GitHub Actions: discovery and security automation.
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
      Security        Intelligence
                         |   |   |
                         |   |   +-- Social
                         |   +------ Market
                         +---------- On-chain/Wallets
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
- SocialMetric
- MLPrediction
- Signal
- Position
- Trade
- Exit
- ModelVersion
- BacktestRun
- SystemEvent

## Security boundaries

Private keys and signing material must never be stored in source code, normal logs or unencrypted configuration. Execution must occur behind a secure signer abstraction.

Live execution must have an explicit feature flag and independent risk gates.

Security providers are evidence sources, not an absolute guarantee. Unknown or contradictory critical security state must result in `DO_NOT_TRADE`.

## Failure philosophy

The default behavior for stale data, uncertain contract state, abnormal liquidity, excessive slippage, RPC/API instability, execution uncertainty or security uncertainty is `DO_NOT_TRADE`.

## Technology candidates

Backend: Python, FastAPI, Pydantic, SQLAlchemy.

Data: PostgreSQL, Redis, Polars/Pandas.

ML: LightGBM/XGBoost, PyTorch.

Execution/data transport: async I/O, WebSockets where supported.

Frontend: React/Next.js/TypeScript.

Deployment: Docker and GitHub Actions.

These are candidate technologies, not immutable requirements; existing BrAInChain architecture must be analyzed before introducing duplicates or incompatible infrastructure.
