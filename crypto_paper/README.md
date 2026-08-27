# Crypto Paper Trading

Phase 6 is a simulation-only execution layer. It consumes signals and models order fills, positions, fees and slippage without connecting to a wallet, RPC signer, DEX router or exchange account.

## Safety boundary

- `TRADING_MODE=paper` is the only supported mode in this package.
- No private key or signing capability is present.
- Security gates cannot be overridden by an opportunity score.
- Position sizing is configurable; the default experimental target is US$0.01.
- If cash, liquidity, exposure or circuit-breaker limits fail, the signal is rejected.
- Paper history is stored outside Firebase.

## Current scope

- signal intake;
- simulated buy fill;
- simulated close;
- position ledger;
- realized/unrealized PnL;
- daily loss and consecutive-loss circuit breakers;
- operational event logging;
- monitoring snapshot.

The package does not claim live-trading readiness. Exit intelligence remains a separate phase.
