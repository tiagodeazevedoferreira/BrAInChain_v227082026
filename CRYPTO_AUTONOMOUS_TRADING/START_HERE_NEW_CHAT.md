# START HERE — Continuação do projeto em um novo chat

## Instrução principal

Você está continuando o desenvolvimento do projeto **Autonomous Crypto Launch Intelligence & Trading** dentro do repositório:

`tiagodeazevedoferreira/BrAInChain_v227082026`

Antes de fazer qualquer alteração:

1. Leia `CRYPTO_AUTONOMOUS_TRADING/PROJECT_CONTEXT.md`.
2. Leia `CRYPTO_AUTONOMOUS_TRADING/ROADMAP.md`.
3. Leia `CRYPTO_AUTONOMOUS_TRADING/ARCHITECTURE.md`.
4. Leia `CRYPTO_AUTONOMOUS_TRADING/DECISIONS.md`.
5. Inspecione o estado real do repositório e do código existente.
6. Identifique em qual fase do roadmap o projeto realmente está.
7. Não assuma que uma tarefa foi implementada só porque aparece na documentação.
8. Não habilite trading real.

## Objetivo do produto

Criar um sistema que descubra novas criptomoedas, analise segurança, liquidez, on-chain, mercado, wallets/smart money e sinais sociais; use Machine Learning para estimar oportunidades de crescimento extremo e risco; faça backtesting e paper trading; e, somente após validação rigorosa e autorização explícita, seja capaz de realizar microoperações automatizadas e gerenciar suas saídas.

## Estratégia conceitual

O sistema deve buscar oportunidades assimétricas, não prever o mercado com certeza.

Pipeline:

`DISCOVERY → SECURITY → INTELLIGENCE → FEATURES → ML → RISK/OPPORTUNITY → DECISION → PAPER → EXIT → LEARNING`

## Princípios inegociáveis

- Segurança precede oportunidade.
- ML alto não supera risco crítico.
- Default em caso de dúvida: `DO_NOT_TRADE`.
- Trading começa em paper mode.
- US$0,01 é um alvo experimental configurável, sujeito a mínimos de ordem, gas, taxas e slippage.
- Nunca contornar regras de DEX/CEX.
- Private keys nunca no código ou Git.
- Live trading nunca é ativado automaticamente.
- Não tentar detectar o pico exato; tratar saída como detecção probabilística de reversão.
- ML deve usar validação temporal e evitar leakage/survivorship bias.
- Modelos em produção não podem se substituir automaticamente sem validação/aprovação.
- Toda decisão deve ser auditável e reproduzível.

## Estado atual

**Fase 1 — Token Discovery: CONCLUÍDA.**

Já existe código funcional em `crypto_discovery/` com:
- adapter GeckoTerminal para novos pools;
- adapter DEX Screener para descoberta complementar;
- modelo normalizado `DiscoveredPool`;
- deduplicação e isolamento de falhas;
- persistência em Firebase RTDB;
- testes unitários;
- smoke test contra APIs reais;
- GitHub Actions a cada 10 minutos;
- verificação read-after-write no Firebase.

A última validação operacional do workflow foi concluída com sucesso: testes, descoberta real, persistência Firebase e leitura de verificação passaram.

## Próxima ação esperada

**Executar a Fase 2 — Security Intelligence de ponta a ponta.**

Primeiro analise as melhores fontes disponíveis e a compatibilidade com as redes/DEXs descobertas na Fase 1. Depois implemente adapters e um Security Engine modular para:

1. inspeção de contrato;
2. honeypot detection;
3. tax/permission analysis;
4. proxy/upgradeability analysis;
5. holder concentration;
6. liquidity lock/removal;
7. Scam/Rug Pull Risk Score.

Não implementar compra real nesta fase. O resultado deve ser um `SecurityAnalysis` auditável e persistido, que será usado como gate obrigatório pelas fases posteriores.

## Critério de continuidade

Quando este arquivo for usado em um novo chat, o agente deve ser capaz de reconstruir o contexto do projeto sem depender do histórico da conversa anterior.

Após cada etapa, atualizar o roadmap e as decisões técnicas relevantes.
