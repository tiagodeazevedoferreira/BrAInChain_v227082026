# Phase 1 — Crypto Discovery Engine

This module implements the first production-oriented slice of BrAInChain's autonomous crypto pipeline.

## Sources

### GeckoTerminal
Uses the public `GET /networks/new_pools` endpoint to discover newly indexed pools across supported networks. The public API is cached and rate-limited, so discovery is intentionally incremental.

### DEX Screener
Uses the latest token profiles endpoint followed by token pair lookup as a complementary discovery signal.

The two sources are deliberately independent. A failure in one source is recorded without discarding successful results from the other.

## Normalized observation

Each discovery observation contains:

- source
- network
- pool address
- base/quote token addresses
- base/quote symbols and names
- DEX
- pool creation time
- USD price
- liquidity
- FDV
- 24h volume
- discovery timestamp
- original source payload

## Firebase layout

The current persistence adapter writes:

```text
discovery/
  status/
    last_run_at
    pool_count
    source_errors
  tokens/
    <network>:<token>:<pool>/
      ...normalized observation...
```

This is an initial operational schema. A later data layer will introduce immutable observation/event storage suitable for ML datasets and historical backtesting.

## Run locally

```bash
cd crypto_discovery
python -m pip install -e ".[test]"
python -m pytest -q
python -m discovery.main --pages 1
```

For Firebase persistence, install the Firebase extra and provide `FIREBASE_SERVICE_ACCOUNT_FILE`.

## Important limitation

"All new cryptocurrencies" cannot be guaranteed by a single public aggregator. Phase 1 therefore uses multiple discovery feeds and an adapter architecture so additional direct chain listeners, DEX indexers and launchpad sources can be added without changing the normalized model or downstream pipeline.
