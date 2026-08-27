# START HERE — Continuação do projeto em um novo chat

## INSTRUÇÃO PRINCIPAL

Você está continuando o desenvolvimento do projeto **Autonomous Crypto Launch Intelligence & Trading** dentro do repositório:

`tiagodeazevedoferreira/BrAInChain_v227082026`

### Ordem obrigatória antes de alterar qualquer coisa

1. Leia `CRYPTO_AUTONOMOUS_TRADING/PROJECT_CONTEXT.md`.
2. Leia `CRYPTO_AUTONOMOUS_TRADING/ROADMAP.md`.
3. Leia `CRYPTO_AUTONOMOUS_TRADING/ARCHITECTURE.md`.
4. Leia `CRYPTO_AUTONOMOUS_TRADING/DECISIONS.md`.
5. Leia `CRYPTO_AUTONOMOUS_TRADING/IMPLEMENTATION_LOG.md`.
6. Inspecione o estado real do repositório e do código existente.
7. Identifique a fase atual pelo código, testes e evidências reais.
8. Não assuma que uma tarefa foi implementada só porque aparece na documentação.
9. Não habilite trading real sem as pré-condições e autorização explícita.

## PREMISSA DE AUTONOMIA

O agente tem autonomia para tomar decisões técnicas, criar/alterar arquivos, configurar dependências e workflows, executar testes, investigar falhas, corrigir, validar e avançar para a próxima etapa sem pedir decisões rotineiras ao usuário.

O usuário só deve ser acionado quando existir um bloqueio que exija ação manual, como credencial, autorização externa, 2FA/CAPTCHA, conexão de serviço/carteira ou operação que as ferramentas disponíveis não possam executar.

## PREMISSA DE MEMÓRIA PERSISTENTE

A pasta `CRYPTO_AUTONOMOUS_TRADING/` é a memória técnica oficial do projeto. Após toda etapa relevante, ela deve ser atualizada com estado real, decisões, testes, limitações e próximo passo.

## OBJETIVO DO PRODUTO

Criar um sistema independente que descubra novas criptomoedas, analise segurança, liquidez, on-chain, mercado, wallets/smart money e sinais sociais; use Machine Learning para estimar oportunidades de crescimento extremo e risco; faça backtesting e paper trading; e, somente após validação rigorosa e autorização explícita, seja capaz de realizar microoperações automatizadas e gerenciar suas saídas.

## PIPELINE

`DISCOVERY → SECURITY → INTELLIGENCE → HISTORICAL DATA → FEATURES → ML → VALIDATION → RISK/OPPORTUNITY → BACKTEST → PAPER → EXIT → LEARNING`

## PRINCÍPIOS INEGOCIÁVEIS

- Segurança precede oportunidade.
- ML alto não supera risco crítico.
- Default em caso de dúvida: `DO_NOT_TRADE`.
- Trading começa em paper mode.
- US$0,01 é um alvo experimental configurável, sujeito a mínimos de ordem, gas, taxas e slippage.
- Nunca contornar regras de DEX/CEX.
- Private keys nunca no código ou Git.
- Live trading nunca é ativado automaticamente.
- O pico não é conhecido antecipadamente; saída é detecção probabilística de reversão.
- ML usa validação temporal e evita leakage/survivorship bias.
- Modelos em produção não se substituem automaticamente sem validação/aprovação.
- Toda decisão deve ser auditável e reproduzível.
- Firebase RTDB é operational state store, não data lake histórico.

## ESTADO ATUAL

**Fase 1 — Token Discovery: CONCLUÍDA E VALIDADA.**

**Fase 2 — Security Intelligence: CONCLUÍDA E VALIDADA.**

**Fase 3 — Market & On-chain Intelligence: IMPLEMENTADA.**

**Fase 4 — Dataset & Machine Learning: IMPLEMENTADA E VALIDADA.**

**Fase 5 — Backtesting: IMPLEMENTADA E VALIDADA.**

**Fase 6 — Paper Trading: IMPLEMENTADA; validação operacional do workflow pendente.**

### Fase 6 — `crypto_paper/`

Possui:
- entrada de sinais;
- execução de compra simulada;
- fechamento simulado;
- posição/ledger;
- PnL realizado e não realizado;
- fees e slippage;
- security/liquidity/opportunity gates;
- max positions/exposure;
- daily loss e consecutive-loss circuit breakers;
- logging e monitoramento;
- histórico fora do Firebase;
- nenhuma capacidade de assinar ou enviar transações reais.

O workflow é `.github/workflows/crypto-paper.yml`.

## PRÓXIMA AÇÃO

Após a validação operacional da Fase 6, implementar **Fase 7 — Exit Intelligence**.

Não implementar compra real antes de satisfazer as pré-condições da Fase 8 e obter autorização explícita.

## CRITÉRIO DE CONCLUSÃO

Uma etapa só é concluída operacionalmente quando código, testes, resultados, integração quando aplicável e documentação estiverem atualizados. Uma implementação pode existir antes da validação; nesse caso o estado deve permanecer explicitamente pendente.

## CONTINUIDADE

Ao abrir um novo chat, leia este arquivo e os documentos relacionados antes de trabalhar. Use o estado real do GitHub como fonte de verdade e continue da próxima etapa sem depender do histórico do chat anterior.
