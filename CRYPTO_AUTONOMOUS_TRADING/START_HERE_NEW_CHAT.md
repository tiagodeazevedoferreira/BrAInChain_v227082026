# START HERE — Continuação do projeto em um novo chat

## INSTRUÇÃO PRINCIPAL

Você está continuando o desenvolvimento do projeto **Autonomous Crypto Launch Intelligence & Trading** dentro do repositório `tiagodeazevedoferreira/BrAInChain_v227082026`.

Antes de alterar qualquer coisa:
1. Leia `PROJECT_CONTEXT.md`.
2. Leia `ROADMAP.md`.
3. Leia `ARCHITECTURE.md`.
4. Leia `DECISIONS.md`.
5. Leia `IMPLEMENTATION_LOG.md`.
6. Inspecione o estado real do GitHub e dos testes.
7. Não assuma que a documentação prova implementação.
8. Não habilite trading real sem todas as pré-condições e autorização explícita.

## AUTONOMIA

O agente deve decidir, implementar, testar, corrigir e validar autonomamente. O usuário só deve ser acionado quando houver bloqueio que exija credencial, autorização externa, 2FA/CAPTCHA, conexão de carteira/serviço ou ação não disponível nas ferramentas.

## MEMÓRIA PERSISTENTE

`CRYPTO_AUTONOMOUS_TRADING/` é a memória técnica oficial. Atualize essa pasta após cada etapa relevante com estado real, testes, limitações e próximo passo.

## OBJETIVO

Descobrir novas criptomoedas, analisar segurança, mercado/on-chain e sinais sociais, usar ML para estimar oportunidades de crescimento extremo e risco, fazer backtesting/paper trading e, somente após validação rigorosa e autorização explícita, preparar microoperações automatizadas.

## PIPELINE

`DISCOVERY → SECURITY → INTELLIGENCE → HISTORICAL DATA → FEATURES → ML → VALIDATION → RISK/OPPORTUNITY → BACKTEST → PAPER → EXIT → LIVE SAFETY GATE → LEARNING`

## PRINCÍPIOS INEGOCIÁVEIS

- Segurança precede oportunidade.
- `DO_NOT_TRADE` vence qualquer score de oportunidade.
- Trading começa em paper mode.
- US$0,01 é alvo experimental, sujeito a mínimos de ordem, gas, taxas e slippage.
- Nunca contornar regras de DEX/CEX.
- Private keys nunca no código ou Git.
- Firebase RTDB é operational state store, não data lake histórico.
- O pico é uma hipótese de reversão, não informação conhecida antecipadamente.
- ML usa validação temporal e evita leakage/survivorship bias.
- Produção não faz auto-retraining cego.
- Toda decisão deve ser auditável.
- Live trading nunca é ativado automaticamente.

## ESTADO ATUAL

**Fase 1 — Discovery: CONCLUÍDA E VALIDADA.**

**Fase 2 — Security: CONCLUÍDA E VALIDADA.**

**Fase 3 — Market/On-chain: CONCLUÍDA E VALIDADA.**

**Fase 4 — Dataset/ML: CONCLUÍDA E VALIDADA.**

**Fase 5 — Backtesting: CONCLUÍDA E VALIDADA.**

**Fase 6 — Paper Trading: CONCLUÍDA E VALIDADA.**

**Fase 7 — Exit Intelligence: CONCLUÍDA E VALIDADA.**

**Fase 8 — Restricted Live Micro Trading: safety boundary IMPLEMENTADA; CI PENDENTE.**

### Fase 8 — `crypto_live/`

Contém:
- configuração live separada;
- gate de `TRADING_MODE=live`;
- gate `LIVE_TRADING_ENABLED`;
- autorização explícita do proprietário;
- gates de backtest, out-of-sample, paper, segurança, failure tests e secrets;
- limites de posição/exposição/gas/slippage/perda;
- `LiveExecutor` fail-closed.

**Não existe ainda um approved venue adapter e nenhuma ordem real é enviada.**

## PRÓXIMA AÇÃO

Executar o workflow `.github/workflows/crypto-live.yml` e validar a fronteira de segurança. Depois, produzir evidência empírica robusta de out-of-sample e paper trading antes de considerar qualquer adapter de venue.

## REGRA DE CONCLUSÃO

Uma fase só é verde quando código, testes, integração quando aplicável, execução operacional e documentação estiverem comprovados.
