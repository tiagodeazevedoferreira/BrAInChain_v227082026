# Roadmap — Autonomous Crypto Launch Intelligence & Trading

## Status

Planejamento inicial. Nenhuma funcionalidade de trading real deve ser considerada implementada por este documento.

## Fase 0 — Contexto e arquitetura
- [x] Criar documentação de contexto
- [ ] Analisar código existente do BrAInChain antes de integrar qualquer módulo
- [ ] Definir limites entre componentes existentes e novo domínio crypto
- [ ] Definir ADRs de arquitetura

## Fase 1 — Token Discovery
- [ ] Blockchain adapter interface
- [ ] DEX adapter interface
- [ ] Detecção de novos contratos/tokens
- [ ] Detecção de novos pools/pares
- [ ] Normalização de token metadata
- [ ] Persistência inicial
- [ ] Testes e observabilidade

## Fase 2 — Security Intelligence
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
