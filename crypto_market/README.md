# Phase 3 — Market & On-chain Intelligence

This package enriches discovered tokens with current market and trade intelligence.

## Current capabilities

- DEX Screener pair observation: price, liquidity, volume, transaction counts, price changes, FDV/market cap and boosts.
- GeckoTerminal recent pool trades: trade side, USD volume, price, transaction hash and wallet/address fields when exposed by the provider.
- Buy/sell pressure.
- Momentum and price-acceleration proxies.
- Liquidity and liquidity-turnover metrics.
- Wallet activity proxy and unique-trader count when provider data exposes trader addresses.
- Whale concentration proxy based on largest trade share.
- Smart-money proxy based on net buy behavior; this is explicitly not a claim of historical wallet profitability.
- Pump/manipulation risk heuristics.
- Provider failure isolation and fail-closed behavior.
- Bounded Firebase persistence: only latest state is written; no unbounded per-run history is appended to RTDB.

## Important limitations

Holder **growth** requires at least two observations of holder count. The current Security phase provides a point-in-time holder count, but intentionally does not create an unbounded Firebase history. Therefore Phase 3 reports `holder_growth_score=null` until a bounded baseline or external historical dataset is introduced.

Likewise, smart-money scoring is a proxy until a wallet-history dataset can measure realized performance, persistence and entry timing. No provider gap is converted into a positive signal.

## Data policy

Firebase is an operational state store, not a historical data lake. Historical datasets for ML will be introduced in a later phase using a storage format suitable for growth (for example partitioned Parquet/object storage/DuckDB), with retention and volume controls.

## Sources

The implementation uses the documented DEX Screener pair/token endpoints and GeckoTerminal pool/trade endpoints. GeckoTerminal's public API is cached at approximately one minute and rate-limited; the workflow therefore limits the number of tokens processed per run. See the official API documentation for current limits and endpoint behavior.
