# Roadmap — Autonomous Crypto Launch Intelligence & Trading

## Status

**Fase 1 concluída. Próxima: Fase 2 — Security Intelligence.**

## Regra de governança do projeto

Ao concluir qualquer etapa, atualizar os arquivos desta pasta `CRYPTO_AUTONOMOUS_TRADING/` com o estado real, decisões, testes, limitações e próximo passo. Esta pasta é a memória técnica persistente utilizada para continuar o desenvolvimento em novos chats.

O agente possui autonomia para decidir e implementar as soluções técnicas, testar, corrigir e validar. O usuário só deve ser acionado quando uma execução manual for realmente necessária.

## Fase 0 — Contexto e arquitetura
- [x] Criar documentação de contexto
- [x] Analisar código existente do BrAInChain antes de integrar qualquer módulo
- [x] Definir limites entre componentes existentes e novo domínio crypto
- [x] Definir decisões arquiteturais / ADRs

## Fase 1 — Token Discovery — CONCLUÍDA
- [x] Blockchain/data-provider adapter interface
- [x] DEX discovery adapter interface
- [x] Detecção de novos contratos/tokens
- [x] Detecção de novos pools/pares
- [x] Normalização de token metadata
- [x] Persistência inicial no Firebase RTDB
- [x] Deduplicação entre fontes
- [x] Isolamento de falha por fonte
- [x] Testes unitários de modelo e adapters
- [x] Smoke test contra APIs reais
- [x] Verificação read-after-write no Firebase
- [x] Execução automatizada a cada 10 minutos

Implementação atual:
- GeckoTerminal: novos pools across supported networks, com paginação pública configurável.
- DEX Screener: latest token profiles + pair lookup como fonte complementar.
- Firebase: `discovery/status` e `discovery/tokens/*`.
- GitHub Actions: testes, smoke test, persistência e read-after-write.

Limitação conhecida: nenhum agregador público garante cobertura de literalmente todas as moedas recém-criadas em todas as blockchains. A arquitetura usa múltiplos adapters para permitir adicionar listeners diretos de blockchain, DEXs, launchpads e outros indexadores.

## Fase 2 — Security Intelligence — PRÓXIMA
- [ ] Contract inspection
- [ ] Honeypot detection
- [ ] Tax/permission analysis
- [ ] Proxy/upgradeability analysis
- [ ] Holder concentration
- [ ] Liquidity lock/removal analysis
- [ ] Scam/Rug Pull Risk Score

## Fase 3 — Market & On-chain Intelligence
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

Inicialmente limitar a microposição configurada e respeitar integralmente os mínimos, taxas, gas e slippage da plataforma.

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
