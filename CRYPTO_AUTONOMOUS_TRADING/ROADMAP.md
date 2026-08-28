# Roadmap — Autonomous Crypto Launch Intelligence & Trading

## Status

**Fases 0–9 validadas. Fases 10–15 — fundações implementadas em uma entrega única; execução histórica/retraining e live permanecem condicionados aos gates.**

## Regra de governança

Ao concluir qualquer etapa, atualizar `CRYPTO_AUTONOMOUS_TRADING/` com estado real, decisões, testes, limitações e próximo passo. Esta pasta é a memória técnica persistente para continuidade em novos chats.

## Fases 0–9 — VALIDADAS

- Fase 0 — Arquitetura
- Fase 1 — Token Discovery
- Fase 2 — Security Intelligence
- Fase 3 — Market & On-chain Intelligence
- Fase 4 — Dataset & ML
- Fase 5 — Backtesting
- Fase 6 — Paper Trading
- Fase 7 — Exit Intelligence
- Fase 8 — Restricted Live Safety Boundary
- Fase 9 — Continuous Learning

## Fases 10–15 — PLANO E FUNDAÇÕES IMPLEMENTADAS

### Fase 10 — Historical Data Expansion — Fundação 🟡
- [x] Outcome/monitoring data contracts
- [x] Append-only learning architecture
- [x] Histórico fora do Firebase como princípio
- [ ] Coleta histórica em escala
- [ ] Auditoria de cobertura/qualidade

### Fase 11 — ML Evaluation & Calibration — Fundação 🟡
- [x] Classification metrics
- [x] OOS evaluation contract
- [x] Baseline-compatible metrics
- [x] Targets no dashboard
- [ ] Treinamento de candidatos em dataset real
- [ ] Probability calibration
- [ ] Estatística de confiança

### Fase 12 — Walk-Forward Validation — Fundação 🟡
- [x] Temporal split
- [x] Walk-forward window helper
- [x] Embargo support
- [ ] Execução sobre dataset real
- [ ] Stability by market regime

### Fase 13 — Long-Running Paper Trading — Fundação 🟡
- [x] Paper engine existente
- [x] Outcome schema
- [x] Monitoring contracts
- [ ] Período contínuo de observação
- [ ] Evidência estatística sustentada

### Fase 14 — Live Trading Readiness Gate — Implementado 🟢 como gate fail-closed
- [x] Data quality gate
- [x] Sample size gate
- [x] OOS gate
- [x] Walk-forward gate
- [x] Paper gate
- [x] Security gate
- [x] Failure-test gate
- [x] Secrets gate
- [x] Circuit-breaker gate
- [x] Venue gate
- [x] Explicit owner approval gate
- [x] Readiness requires ALL gates
- [ ] Any real-live approval

### Fase 15 — Micro-Live Executor — Safety Boundary 🟢 / Executor real 🔴
- [x] Parameterized target trade size
- [x] Exposure concept
- [x] Isolated executor architecture from Phase 8
- [x] Fail-closed behavior
- [ ] Venue adapter
- [ ] Wallet/signing
- [ ] Real BUY/SELL

## ML Monitoring Dashboard

`ML_MONITORING/` é o frontend PWA inicial.

- Atualização padrão: 5 minutos.
- Estado de paper pode futuramente ter feed de 1 minuto.
- Exibe métricas, metas, readiness gate e parâmetros.
- Valor de operação é configurável no frontend; US$0,01 é apenas valor inicial, não compromisso.
- Persistência do parâmetro no navegador via localStorage.
- O dashboard não possui permissão de executar ordens.

### Metas iniciais

| Indicador | Meta inicial | Direção |
|---|---:|---|
| Precision | ≥ 60% | maior |
| Recall | ≥ 50% | maior |
| Balanced Accuracy | ≥ 60% | maior |
| Mean Return líquido | > 0% | maior |
| Max Drawdown | ≤ 25% | menor |
| Peak Capture | ≥ 70% | maior |
| 2x Detection | ≥ 70% | maior |
| 5x Detection | ≥ 60% | maior |
| 10x Detection | ≥ 40% | maior |

As metas são metas iniciais de engenharia. Não representam promessa de retorno e serão recalibradas com dados reais e intervalos de confiança.

## Workflows novos

- `Crypto ML Monitoring & Readiness` — testes do monitoring e prova de fail-closed.
- `Crypto Continuous Learning` — testes de aprendizado/governança.

## Calendário resumido

Semanas 1–3: Fase 10
Semanas 4–6: Fase 11
Semanas 7–9: Fase 12
Semanas 10–14: Fase 13
Semanas 15–16: Fase 14
Semanas 17–18+: Fase 15

As semanas são planejamento e podem ser estendidas caso a evidência estatística seja insuficiente.

## Regras de segurança

- Live trading nunca é ativado automaticamente.
- Private keys nunca ficam no código, logs ou configuração não protegida.
- Firebase não recebe histórico ilimitado.
- Não assumir que US$0,01 é economicamente executável.
- A ordem futura deverá respeitar minimum order, gas, slippage, price impact e exposição.
- Em caso de dúvida crítica: `DO_NOT_TRADE`.

## Regra de avanço

Uma fase só é marcada como validada quando houver código funcional, testes, evidência operacional e documentação correspondente.
