# Roadmap — Autonomous Crypto Launch Intelligence & Trading

## Status

**Fase 9 — Continuous Learning implementada; validação operacional do workflow pendente.**

## Regra de governança

Ao concluir qualquer etapa, atualizar `CRYPTO_AUTONOMOUS_TRADING/` com o estado real, decisões, testes, limitações e próximo passo. Esta pasta é a memória técnica persistente para continuidade em novos chats.

## Fases concluídas e validadas

### Fase 0 — Contexto e arquitetura — CONCLUÍDA
### Fase 1 — Token Discovery — CONCLUÍDA E VALIDADA
### Fase 2 — Security Intelligence — CONCLUÍDA E VALIDADA
### Fase 3 — Market & On-chain Intelligence — CONCLUÍDA E VALIDADA; CI RECENTEMENTE CORRIGIDA
### Fase 4 — Dataset & Machine Learning — CONCLUÍDA E VALIDADA
### Fase 5 — Backtesting — CONCLUÍDA E VALIDADA
### Fase 6 — Paper Trading — CONCLUÍDA E VALIDADA
### Fase 7 — Exit Intelligence — CONCLUÍDA E VALIDADA

## Fase 8 — Restricted Live Micro Trading — SAFETY BOUNDARY IMPLEMENTADA E VALIDADA
- [x] Explicit live mode/owner/evidence gates
- [x] Position/exposure/gas/slippage/loss limits
- [x] Fail-closed live executor
- [x] No approved venue adapter
- [x] CI validated
- [ ] Actual live authorization
- [ ] Actual order execution

## Fase 9 — Continuous Learning — IMPLEMENTADA; CI PENDENTE

### Dataset de resultados
- [x] Outcome schema
- [x] Model/feature version tracking
- [x] Entry/peak/exit/return/drawdown/peak-capture tracking
- [x] Market regime field
- [x] Append-only local learning journal
- [x] No unbounded Firebase historical storage

### Validação temporal
- [x] Chronological train/validation/test split
- [x] No random split
- [x] Embargo helper for forward-labelled samples
- [x] Boundary rounding corrected for small datasets

### Model governance
- [x] Candidate evaluation gate
- [x] Minimum sample gate
- [x] Balanced accuracy gate
- [x] Positive-return gate
- [x] Drawdown ceiling
- [x] Champion/challenger comparison
- [x] Strict promotion requirement
- [x] No automatic live promotion
- [ ] Production rollback artifact
- [ ] Full retraining orchestration
- [ ] Regime-specific calibration

### CI
- [x] Unit tests
- [x] `Crypto Continuous Learning` workflow
- [x] `workflow_dispatch`
- [ ] Operational CI validation

## Próxima etapa após validar a Fase 9

Executar aprendizado contínuo com dados reais do Paper Trading, construir retraining/calibration sobre dataset suficientemente grande e estabelecer evidência out-of-sample. Depois disso, podemos retornar à camada de execução e implementar, de forma isolada, um venue adapter para compra/venda real.

## Regras de segurança

- Live trading nunca é ativado automaticamente.
- Private keys nunca ficam no código, logs ou configuração não protegida.
- Firebase não recebe histórico ilimitado.
- US$0,01 é alvo experimental e pode ser inviável em determinados venues.
- Não contornar mínimos de ordem, gas, slippage ou regras de DEX/CEX.
- Em caso de dúvida crítica: `DO_NOT_TRADE`.

## Regra de avanço

Uma fase só é concluída quando houver código funcional, testes, evidência operacional e documentação correspondente.
