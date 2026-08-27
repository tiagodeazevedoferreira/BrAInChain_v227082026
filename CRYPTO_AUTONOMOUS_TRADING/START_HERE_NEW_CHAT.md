# START HERE — Continuação do projeto em um novo chat

## INSTRUÇÃO PRINCIPAL

Você está continuando o desenvolvimento do projeto **Autonomous Crypto Launch Intelligence & Trading** dentro do repositório:

`tiagodeazevedoferreira/BrAInChain_v227082026`

### Ordem obrigatória antes de alterar qualquer coisa

1. Leia `CRYPTO_AUTONOMOUS_TRADING/PROJECT_CONTEXT.md`.
2. Leia `CRYPTO_AUTONOMOUS_TRADING/ROADMAP.md`.
3. Leia `CRYPTO_AUTONOMOUS_TRADING/ARCHITECTURE.md`.
4. Leia `CRYPTO_AUTONOMOUS_TRADING/DECISIONS.md`.
5. Inspecione o estado real do repositório e do código existente.
6. Identifique a fase atual pelo código, testes e evidências reais.
7. Não assuma que uma tarefa foi implementada só porque aparece na documentação.
8. Não habilite trading real sem as pré-condições e autorização explícita.

## PREMISSA DE AUTONOMIA

O agente tem autonomia para tomar decisões técnicas, criar/alterar arquivos, configurar dependências e workflows, executar testes, investigar falhas, corrigir, validar e avançar para a próxima etapa sem pedir decisões rotineiras ao usuário.

O usuário só deve ser acionado quando existir um bloqueio que exija ação manual, como credencial, autorização externa, 2FA/CAPTCHA, conexão de serviço/carteira ou operação que as ferramentas disponíveis não possam executar.

## PREMISSA DE MEMÓRIA PERSISTENTE

A pasta `CRYPTO_AUTONOMOUS_TRADING/` é a memória técnica oficial do projeto.

**Após toda etapa relevante, é obrigatório atualizar esta pasta com o que realmente foi feito.** No mínimo, atualizar quando aplicável:

- `PROJECT_CONTEXT.md` — estado atual e premissas;
- `ROADMAP.md` — tarefas concluídas e próxima fase;
- `ARCHITECTURE.md` — mudanças arquiteturais;
- `DECISIONS.md` — novas decisões/ADRs;
- `IMPLEMENTATION_LOG.md` — implementação, arquivos, testes, resultados, limitações e próximos passos.

Nunca encerrar uma etapa sem registrar seu estado no GitHub.

## OBJETIVO DO PRODUTO

Criar um sistema que descubra novas criptomoedas, analise segurança, liquidez, on-chain, mercado, wallets/smart money e sinais sociais; use Machine Learning para estimar oportunidades de crescimento extremo e risco; faça backtesting e paper trading; e, somente após validação rigorosa e autorização explícita, seja capaz de realizar microoperações automatizadas e gerenciar suas saídas.

## PIPELINE

`DISCOVERY → SECURITY → INTELLIGENCE → FEATURES → ML → RISK/OPPORTUNITY → DECISION → PAPER → EXIT → LEARNING`

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

## ESTADO ATUAL

**Fase 1 — Token Discovery: CONCLUÍDA.**

Existe código funcional em `crypto_discovery/` com adapters para GeckoTerminal e DEX Screener, modelo normalizado `DiscoveredPool`, deduplicação, isolamento de falhas, persistência Firebase RTDB, testes, smoke test contra APIs reais, GitHub Actions a cada 10 minutos e read-after-write no Firebase.

A integração GitHub Actions → Firebase foi validada operacionalmente com conexão, escrita e leitura bem-sucedidas.

**Próxima fase: Fase 2 — Security Intelligence.**

## PRÓXIMA AÇÃO

Executar a Fase 2 de ponta a ponta. Antes de implementar, pesquisar/avaliar as fontes disponíveis e sua compatibilidade com as redes/DEXs descobertas. Implementar um Security Engine modular e auditável para inspeção de contrato, honeypot detection, taxes/permissions, proxy/upgradeability, holder concentration, liquidity lock/removal e Scam/Rug Pull Risk Score.

Não implementar compra real nesta fase.

## CRITÉRIO DE CONCLUSÃO DE UMA ETAPA

Uma etapa só é concluída quando:

1. código funcional foi criado/alterado;
2. testes relevantes foram executados;
3. resultados foram analisados;
4. falhas foram corrigidas quando possível;
5. integração foi validada quando aplicável;
6. documentação desta pasta foi atualizada;
7. roadmap foi atualizado;
8. limitações conhecidas foram registradas;
9. próximo passo ficou definido.

## CONTINUIDADE

Ao abrir um novo chat, leia este arquivo e os quatro documentos relacionados antes de trabalhar. Use o estado real do GitHub como fonte de verdade e continue da próxima etapa sem depender do histórico do chat anterior.
