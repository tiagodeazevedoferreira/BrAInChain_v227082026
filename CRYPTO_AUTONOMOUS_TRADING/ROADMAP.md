# Roadmap — Autonomous Crypto Launch Intelligence & Trading

## Status

**Fase 3 implementada; validação operacional do workflow em andamento. Próxima: Fase 4 — Dataset & Machine Learning.**

## Regra de governança do projeto

Ao concluir qualquer etapa, atualizar os arquivos desta pasta `CRYPTO_AUTONOMOUS_TRADING/` com o estado real, decisões, testes, limitações e próximo passo. Esta pasta é a memória técnica persistente utilizada para continuar o desenvolvimento em novos chats.

O agente possui autonomia para decidir e implementar as soluções técnicas, testar, corrigir e validar. O usuário só deve ser acionado quando uma execução manual for realmente necessária.

## Fase 0 — Contexto e arquitetura
- [x] Contexto e arquitetura
- [x] Premissas de autonomia e memória persistente
- [x] Firebase + GitHub Actions

## Fase 1 — Token Discovery — CONCLUÍDA
- [x] Descoberta GeckoTerminal
- [x] Descoberta complementar DEX Screener
- [x] Modelo normalizado
- [x] Deduplicação
- [x] Isolamento de falha
- [x] Firebase RTDB
- [x] Testes e smoke test
- [x] Workflow automático a cada 10 minutos

## Fase 2 — Security Intelligence — CONCLUÍDA E VALIDADA
- [x] `SecurityAnalysis` auditável
- [x] Honeypot simulation via Honeypot.is
- [x] Buy/sell/transfer tax analysis
- [x] Simulation success/failure
- [x] Holder sell-failure and siphoning indicators
- [x] Contract source/open-source analysis
- [x] Proxy/proxy-call analysis
- [x] Top-holder and top-5 concentration
- [x] Optional GoPlus Token Security adapter
- [x] Deterministic Scam/Rug Pull Risk Score
- [x] Hard security gate `DO_NOT_TRADE`
- [x] Firebase persistence em `security/tokens/*`
- [x] Incremental processing
- [x] Unit/integration tests
- [x] GitHub Actions automático
- [x] Firebase credential cleanup
- [x] CI isolation/default fixes
- [x] Operational validation

## Fase 3 — Market & On-chain Intelligence — IMPLEMENTADA
- [x] Price/volume observation
- [x] Buy/sell transaction pressure
- [x] Momentum and price-acceleration proxies
- [x] Liquidity and liquidity-turnover metrics
- [x] Trade-level wallet activity when provider exposes trader addresses
- [x] Whale concentration proxy using largest trade share
- [x] Smart-money behavior proxy using net-buy pressure
- [x] Pump/manipulation heuristics
- [x] Provider failure isolation
- [x] Fail-closed decision behavior
- [x] Bounded Firebase latest-state persistence
- [x] Unit tests
- [x] Engine tests
- [x] GitHub Actions every 10 minutes + manual dispatch

### Fase 3 — Limitações deliberadas
- Holder growth is `null` until a bounded baseline or external historical dataset exists. A single point-in-time holder count cannot establish growth.
- Smart-money is a proxy, not wallet-profitability intelligence. Full smart-money scoring requires wallet history and outcome labels.
- Whale detection is trade-concentration based and complements, rather than replaces, security holder concentration.
- Firebase is not used for historical snapshots.

### Fase 3 — Evidência CI
Workflow `Crypto Market & On-chain Intelligence` foi criado e o primeiro run identificou uma expectativa incorreta no teste de concentração de whale; a falha foi corrigida no commit seguinte. A execução corretiva está sendo validada antes de marcar a fase como operacionalmente concluída.

## Fase 4 — Dataset & Machine Learning
- [ ] Historical dataset builder
- [ ] Storage strategy for historical data (Parquet/object storage/DuckDB or equivalent)
- [ ] Winner/loser/scam/rug-pull labels
- [ ] Multi-horizon labels (+10/+25/+50/+100/+500/+1000%, crash/rug)
- [ ] Time-aware feature engineering
- [ ] Baseline models
- [ ] Ensemble comparison
- [ ] Calibration
- [ ] Walk-forward validation
- [ ] Out-of-sample evaluation
- [ ] Model registry/versioning

## Fase 5 — Backtesting
- [ ] Event-driven backtester
- [ ] Fees
- [ ] Gas
- [ ] Slippage
- [ ] Latency
- [ ] Failed transactions
- [ ] Entry strategies
- [ ] Exit strategies
- [ ] Risk-adjusted metrics

## Fase 6 — Paper Trading
- [ ] Real-time signal generation
- [ ] Simulated execution
- [ ] Position ledger
- [ ] PnL
- [ ] Exit engine
- [ ] Alerts
- [ ] Operational monitoring

## Fase 7 — Exit Intelligence
- [ ] Trailing stop
- [ ] Dynamic take profit
- [ ] Momentum reversal
- [ ] Volume reversal
- [ ] Whale exit
- [ ] Liquidity deterioration
- [ ] Crash protection
- [ ] Time stop
- [ ] Probabilistic peak/reversal detection

## Fase 8 — Restricted Live Micro Trading
Pré-condições obrigatórias:
- [ ] Backtesting satisfatório
- [ ] Out-of-sample satisfatório
- [ ] Paper trading satisfatório
- [ ] Security tests aprovados
- [ ] Failure tests aprovados
- [ ] Secrets/signing seguros
- [ ] Circuit breakers ativos
- [ ] Autorização explícita do proprietário

## Fase 9 — Continuous Learning
- [ ] Trade outcome dataset
- [ ] Retraining pipeline
- [ ] Model comparison
- [ ] Champion/challenger
- [ ] Model approval gate
- [ ] Rollback
- [ ] Strategy/threshold optimization
- [ ] Regime monitoring

## Regra de avanço

Não pular fases. Uma fase só é considerada concluída quando houver código funcional, testes, evidência operacional e documentação correspondente.
