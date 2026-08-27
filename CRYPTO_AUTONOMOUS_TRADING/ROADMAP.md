# Roadmap — Autonomous Crypto Launch Intelligence & Trading

## Status

**Fase 8 — Restricted Live Micro Trading: safety boundary implementada; validação operacional do workflow pendente.**

## Regra de governança

Ao concluir qualquer etapa, atualizar `CRYPTO_AUTONOMOUS_TRADING/` com o estado real, decisões, testes, limitações e próximo passo. Esta pasta é a memória técnica persistente para continuidade em novos chats.

## Fases concluídas

### Fase 0 — Contexto e arquitetura — CONCLUÍDA
- [x] Contexto e arquitetura
- [x] Autonomia e memória persistente
- [x] Firebase + GitHub Actions

### Fase 1 — Token Discovery — CONCLUÍDA E VALIDADA
- [x] GeckoTerminal / DEX Screener
- [x] Normalização / deduplicação
- [x] Tolerância a falhas
- [x] Firebase RTDB
- [x] Testes / smoke test / workflow

### Fase 2 — Security Intelligence — CONCLUÍDA E VALIDADA
- [x] Honeypot, taxes, simulations
- [x] Contract/source/proxy analysis
- [x] Holder analysis
- [x] Deterministic risk score
- [x] Hard `DO_NOT_TRADE`
- [x] Firebase incremental persistence
- [x] CI validado

### Fase 3 — Market & On-chain Intelligence — CONCLUÍDA E VALIDADA
- [x] Price/volume
- [x] Buy/sell pressure
- [x] Momentum/acceleration
- [x] Liquidity/turnover
- [x] Trade wallet activity
- [x] Whale concentration proxy
- [x] Smart-money proxy
- [x] Manipulation heuristics
- [x] Fail-closed
- [x] Bounded Firebase state

### Fase 4 — Dataset & Machine Learning — CONCLUÍDA E VALIDADA
- [x] ML contracts
- [x] Historical JSONL outside Firebase
- [x] Forward multi-horizon labels
- [x] Growth/crash labels
- [x] Time-local features
- [x] Readiness gate
- [x] Research baseline
- [x] Tests / CI

### Fase 5 — Backtesting — CONCLUÍDA E VALIDADA
- [x] Event-driven backtester
- [x] Fees / gas / slippage
- [x] Security / score / liquidity gates
- [x] Trade journal
- [x] PnL / metrics
- [x] Tests / CI

### Fase 6 — Paper Trading — CONCLUÍDA E VALIDADA
- [x] Simulated execution
- [x] Position ledger / PnL
- [x] Fees / slippage
- [x] Security / liquidity / opportunity gates
- [x] Exposure / position limits
- [x] Daily / consecutive loss breakers
- [x] Monitoring / logging
- [x] Historical storage outside Firebase
- [x] No signing or live transport
- [x] CI validated

### Fase 7 — Exit Intelligence — CONCLUÍDA E VALIDADA
- [x] Trailing stop
- [x] Dynamic take profit + reversal confirmation
- [x] Momentum / volume reversal
- [x] Whale exit contract
- [x] Liquidity deterioration
- [x] Crash protection
- [x] Time stop
- [x] Exit score
- [x] Peak capture
- [x] Tests / CI validated

## Fase 8 — Restricted Live Micro Trading — IMPLEMENTADA; CI PENDENTE

### Safety boundary
- [x] `LiveConfig`
- [x] Explicit `TRADING_MODE=live` gate
- [x] `LIVE_TRADING_ENABLED` gate
- [x] Explicit owner authorization gate
- [x] Backtest evidence gate
- [x] Out-of-sample evidence gate
- [x] Paper evidence gate
- [x] Security tests gate
- [x] Failure tests gate
- [x] Secure signing/secret configuration gate
- [x] Position/exposure limits
- [x] Gas/slippage limits
- [x] Daily/consecutive loss limits
- [x] Fail-closed `LiveExecutor`
- [x] CI workflow with `workflow_dispatch`
- [ ] Operational CI validation
- [ ] Approved venue adapter
- [ ] Actual live authorization

### Important
A CI-green Phase 8 only proves that the safety boundary works. It does not prove profitability and does not authorize real-money trading.

Before an approved venue adapter is implemented, the project must produce empirical out-of-sample and sustained paper-trading evidence. No live order is sent by the current code.

## Fase 9 — Continuous Learning
- [ ] Trade outcome dataset
- [ ] Retraining pipeline
- [ ] Model comparison
- [ ] Champion/challenger
- [ ] Model approval gate
- [ ] Rollback
- [ ] Strategy/threshold optimization
- [ ] Regime monitoring

## Regras de segurança

- Live trading nunca é ativado automaticamente.
- Private keys nunca ficam no código, logs ou configuração não protegida.
- Firebase não recebe histórico ilimitado.
- US$0,01 é alvo experimental e pode ser inviável em determinados venues.
- Não contornar mínimos de ordem, gas, slippage ou regras de DEX/CEX.
- Em caso de dúvida crítica: `DO_NOT_TRADE`.

## Regra de avanço

Uma fase só é concluída quando houver código funcional, testes, evidência operacional e documentação correspondente.
