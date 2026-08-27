# Roadmap — Autonomous Crypto Launch Intelligence & Trading

## Status

**Fase 2 concluída em implementação e validação operacional; próxima: Fase 3 — Market & On-chain Intelligence.**

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
- [x] Incremental processing: somente tokens ainda não analisados
- [x] Unit tests
- [x] Engine integration tests
- [x] GitHub Actions automático a cada 10 minutos
- [x] Firebase credential cleanup no runner
- [x] Correção de isolamento do pytest no CI
- [x] Correção dos defaults de `SecurityAnalysis`
- [x] Validação operacional de workflow

### Evidência de validação da Fase 2
Workflow run **#8 / 33116891066**:
- `test` → success;
- `security-scan` → success;
- `SECURITY_INPUT=25`;
- `SECURITY_ANALYZED=25`;
- `SECURITY_DO_NOT_TRADE=25`;
- `SECURITY_CRITICAL=0`;
- `SECURITY_PIPELINE=OK`.

Os 25 tokens foram bloqueados para negociação pelas regras conservadoras atuais; isso não significa que todos sejam honeypots. O sistema está deliberadamente em modo fail-safe.

### Fase 2 — limitações conhecidas
- Liquidity lock/removal permanece `unknown` quando não há evidência confiável de locker; o sistema não presume segurança.
- GoPlus é opcional e só é consultado quando `GOPLUS_ACCESS_TOKEN` está configurado.
- Honeypot/security providers não são auditoria formal de smart contract e podem ter cobertura/latência diferentes por chain.
- Tokens em chains não suportadas ficam bloqueados (`DO_NOT_TRADE`).
- Nenhum mecanismo de segurança é considerado infalível.

## Fase 3 — Market & On-chain Intelligence — PRÓXIMA
- [ ] Price/volume snapshots
- [ ] Holder growth
- [ ] Buy/sell pressure
- [ ] Wallet activity
- [ ] Whale detection
- [ ] Smart Money scoring
- [ ] Momentum/volatility/liquidity metrics
- [ ] Pump/manipulation detection

## Fase 4 — Dataset & Machine Learning
- [ ] Historical dataset builder
- [ ] Winner/loser/scam/rug-pull labels
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
