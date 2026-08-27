# Roadmap — Autonomous Crypto Launch Intelligence & Trading

## Status

**Fase 6 — Paper Trading implementada; validação operacional do workflow pendente.**

## Regra de governança do projeto

Ao concluir qualquer etapa, atualizar os arquivos desta pasta `CRYPTO_AUTONOMOUS_TRADING/` com o estado real, decisões, testes, limitações e próximo passo. Esta pasta é a memória técnica persistente utilizada para continuar o desenvolvimento em novos chats.

O agente possui autonomia para decidir e implementar as soluções técnicas, testar, corrigir e validar. O usuário só deve ser acionado quando uma execução manual for realmente necessária.

## Fase 0 — Contexto e arquitetura — CONCLUÍDA
- [x] Contexto e arquitetura
- [x] Premissas de autonomia e memória persistente
- [x] Firebase + GitHub Actions

## Fase 1 — Token Discovery — CONCLUÍDA E VALIDADA
- [x] GeckoTerminal
- [x] DEX Screener
- [x] Normalização
- [x] Deduplicação
- [x] Isolamento de falha
- [x] Firebase RTDB
- [x] Testes e smoke test
- [x] Workflow automático

## Fase 2 — Security Intelligence — CONCLUÍDA E VALIDADA
- [x] Honeypot, taxes e simulations
- [x] Contract/source/proxy analysis
- [x] Holder analysis
- [x] Deterministic risk score
- [x] Hard `DO_NOT_TRADE` gate
- [x] Firebase persistence e processamento incremental
- [x] Unit/integration tests
- [x] CI e validação operacional

## Fase 3 — Market & On-chain Intelligence — IMPLEMENTADA
- [x] Price/volume
- [x] Buy/sell pressure
- [x] Momentum/acceleration proxies
- [x] Liquidity/turnover
- [x] Trade wallet activity
- [x] Whale concentration proxy
- [x] Smart-money proxy
- [x] Manipulation heuristics
- [x] Fail-closed behavior
- [x] Bounded Firebase current state

## Fase 4 — Dataset & Machine Learning — IMPLEMENTADA E VALIDADA
- [x] ML sample contract
- [x] Historical JSONL storage abstraction outside Firebase
- [x] Forward multi-horizon labels
- [x] Growth and crash labels
- [x] Time-local feature extraction
- [x] Readiness gate
- [x] Research baseline
- [x] Tests
- [x] GitHub Actions

## Fase 5 — Backtesting — IMPLEMENTADA E VALIDADA
- [x] Event-driven backtester
- [x] Fees
- [x] Gas
- [x] Slippage
- [x] Security/score/liquidity gates
- [x] Trade journal
- [x] PnL and summary metrics
- [x] Unit tests
- [x] GitHub Actions

## Fase 6 — Paper Trading — IMPLEMENTADA; CI PENDENTE
- [x] Real-time-style signal intake
- [x] Simulated buy execution
- [x] Position ledger
- [x] Realized/unrealized PnL
- [x] Fee/slippage simulation
- [x] Security hard gate
- [x] Liquidity/opportunity gates
- [x] Max positions/exposure controls
- [x] Daily loss circuit breaker
- [x] Consecutive-loss circuit breaker
- [x] Operational event logging
- [x] Monitoring snapshot
- [x] Paper history outside Firebase
- [x] No wallet/RPC/DEX/CEX signing capability
- [x] GitHub Actions manual dispatch
- [ ] Operational CI validation

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

## Regras de segurança

- Não existe execução real neste módulo.
- `TRADING_MODE=paper` é obrigatório para esta fase.
- Private keys não são aceitas.
- Firebase não recebe histórico ilimitado.
- Em caso de dúvida crítica: `DO_NOT_TRADE`.
- Live trading não é ativado automaticamente.

## Regra de avanço

Uma fase só é concluída quando houver código funcional, testes, evidência operacional e documentação correspondente.
