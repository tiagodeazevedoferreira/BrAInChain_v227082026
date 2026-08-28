# Fases 10–15 — Plano Executivo

## Objetivo
Transformar a fundação atual em evidência estatística, monitoramento contínuo e, somente no fim, uma camada de execução micro-live isolada.

| Fase | Janela | Objetivo | Saída | Critério de avanço |
|---|---|---|---|---|
| 10 | Semanas 1–3 | Historical Data Expansion | Dataset de observações e outcomes com qualidade controlada | volume, cobertura e qualidade mínimos definidos e medidos |
| 11 | Semanas 4–6 | ML Evaluation & Calibration | benchmark, probabilidades calibradas e métricas por horizonte | OOS reproduzível e retorno líquido não negativo |
| 12 | Semanas 7–9 | Walk-Forward Validation | avaliação rolling e estabilidade por regime | desempenho consistente em janelas independentes |
| 13 | Semanas 10–14 | Long-Running Paper Trading | operação contínua sem dinheiro real | estabilidade operacional + performance líquida sustentada |
| 14 | Semanas 15–16 | Live Trading Readiness Gate | decisão formal de prontidão | todos os gates críticos verdes + aprovação explícita |
| 15 | Semanas 17–18+ | Micro-Live Executor | adaptador de venue isolado | somente após Fase 14; limites e kill switch ativos |

## Cadência

- Discovery/market monitoring: contínuo, conforme workflows existentes.
- Dashboard ML: refresh de 5 minutos por padrão.
- Estado paper: até 1 minuto quando necessário.
- Relatórios de modelo: diariamente ou a cada novo lote de outcomes suficiente para avaliação.
- Retraining: por lote mínimo de dados, nunca apenas por relógio.
- Readiness: recalculado após cada nova avaliação significativa.

## Metas iniciais do dashboard

- Precision: >= 60%
- Recall: >= 50%
- Balanced Accuracy: >= 60%
- Mean Return: > 0% após custos
- Max Drawdown: <= 25%
- Peak Capture: >= 70%
- 2x Detection: >= 70%
- 5x Detection: >= 60%
- 10x Detection: >= 40%

Essas são metas iniciais de engenharia, não promessa de retorno. Serão recalibradas conforme a distribuição real dos eventos e os intervalos de confiança.

## Fase 10 — Historical Data Expansion
1. Capturar snapshots em decisão-time.
2. Preservar tokens que falham, somem, sofrem rug ou perdem liquidez.
3. Gerar labels em múltiplos horizontes.
4. Validar completude, duplicação, timestamps e leakage.
5. Manter histórico fora do Firebase RTDB.

## Fase 11 — ML Evaluation & Calibration
1. Benchmark contra baseline ingênuo.
2. Treinar candidatos com features versionadas.
3. Calibrar probabilidades.
4. Avaliar precision, recall, balanced accuracy e matriz de confusão.
5. Medir retorno líquido, drawdown e peak capture.
6. Separar resultados por 2x/5x/10x e por regime.

## Fase 12 — Walk-Forward Validation
1. Janelas temporais rolling.
2. Purge/embargo para labels forward.
3. Nunca usar futuro no treino.
4. Consolidar média, dispersão e pior janela.
5. Rejeitar modelos que dependam de uma única janela/regime.

## Fase 13 — Long-Running Paper Trading
1. Alimentar o paper engine continuamente.
2. Registrar cada decisão e outcome.
3. Medir custos simulados de forma conservadora.
4. Exercitar circuit breakers.
5. Comparar Champion vs Challenger sem promoção cega.

## Fase 14 — Live Trading Readiness Gate
Obrigatório:
- dataset e qualidade aprovados;
- OOS aprovado;
- walk-forward aprovado;
- paper trading aprovado;
- security/failure tests aprovados;
- secrets seguros;
- circuit breakers testados;
- venue e minimum order verificados;
- parâmetros econômicos aprovados;
- aprovação explícita do proprietário.

O gate é fail-closed.

## Fase 15 — Micro-Live Executor
A execução real será desenvolvida somente após a aprovação da Fase 14. O primeiro executor deve ser isolado do modelo e aceitar apenas uma decisão assinada/validada pelo risk gate. O tamanho da ordem não é fixado em US$0,01: ele é um parâmetro configurável e deverá respeitar minimum order, gas, slippage, price impact e exposição máxima.

## Dashboard

`ML_MONITORING/` é o frontend inicial PWA. Ele mostra métricas atuais, meta inicial, estado do readiness gate e parâmetros experimentais. O valor de operação é configurável no frontend e, nesta etapa, é apenas parâmetro de monitoramento/paper; não habilita live trading.
