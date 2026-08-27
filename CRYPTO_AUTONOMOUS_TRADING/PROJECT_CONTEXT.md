# BrAInChain — Autonomous Crypto Launch Intelligence & Trading

## CONTEXTO PARA NOVOS CHATS

Este diretório é a memória técnica persistente do projeto. Sempre que o desenvolvimento avançar, esta pasta deve ser atualizada com o estado real, decisões, testes e próximos passos.

**IMPORTANTE:** trading real permanece desabilitado até que todas as pré-condições do roadmap sejam satisfeitas e exista autorização explícita.

## OBJETIVO

Construir progressivamente um sistema capaz de descobrir novas criptomoedas e pools, avaliar segurança e risco, analisar dados de mercado/on-chain/social, utilizar Machine Learning para identificar oportunidades assimétricas, executar backtesting/paper trading e, somente após validação rigorosa, realizar microoperações automatizadas e gerenciar suas saídas.

## PREMISSAS OPERACIONAIS

1. **Autonomia de desenvolvimento:** o agente deve decidir a implementação técnica, criar/alterar código, configurar componentes, testar, corrigir e validar resultados sem pedir decisões pequenas ao usuário.
2. **Intervenção manual somente quando necessária:** o usuário só deve ser acionado quando uma ação depender de credencial, autorização, confirmação externa, 2FA/CAPTCHA, conexão de serviço/carteira ou outra operação que as ferramentas não possam executar.
3. **Memória no GitHub:** ao final de cada etapa, os arquivos desta pasta `CRYPTO_AUTONOMOUS_TRADING/` devem ser atualizados para registrar o estado real do projeto, independentemente do histórico do chat.
4. **Não assumir implementação:** documentação deve refletir somente o que foi realmente implementado e validado.
5. **Segurança antes de retorno:** nenhum score de oportunidade pode ultrapassar um bloqueio crítico de segurança.
6. **Trading real não é desenvolvimento:** autonomia técnica não constitui autorização para movimentar dinheiro real.

## FLUXO PRINCIPAL

DISCOVERY → NORMALIZATION → SECURITY → ON-CHAIN → MARKET → SOCIAL → FEATURES → ML → OPPORTUNITY/RISK → DECISION → PAPER/LIVE EXECUTION → MONITORING → EXIT → POST-TRADE ANALYSIS → LEARNING

## ARQUITETURA PREVISTA

- Python
- FastAPI
- PostgreSQL
- Redis
- workers assíncronos/event-driven
- WebSockets quando disponíveis
- PyTorch
- LightGBM/XGBoost
- Pandas/Polars
- SQLAlchemy
- Pydantic
- Docker
- GitHub Actions
- Frontend React/Next.js/TypeScript

São tecnologias candidatas. Antes de introduzir qualquer uma, analisar e reaproveitar a infraestrutura existente do BrAInChain quando fizer sentido.

## MÓDULOS PLANEJADOS

- discovery/
- blockchain/
- dex/
- security/
- onchain/
- market/
- wallets/
- social/
- features/
- ml/
- backtesting/
- strategy/
- execution/
- portfolio/
- risk/
- notifications/
- monitoring/

## ESTADO IMPLEMENTADO

### Fase 1 — Discovery

Implementado em `crypto_discovery/`: GeckoTerminal + DEX Screener, normalização, deduplicação, tolerância a falhas, Firebase e GitHub Actions a cada 10 minutos.

### Fase 2 — Security Intelligence

Implementado em `crypto_security/`:

- `SecurityAnalysis` auditável;
- Honeypot.is simulation/honeypot checks;
- buy/sell/transfer tax analysis;
- simulation success/failure;
- holder sell failures and siphoning;
- contract source/open-source verification;
- proxy/proxy-call detection;
- top-holder/top-5 concentration;
- optional GoPlus Token Security provider;
- deterministic risk score;
- critical flags/warnings;
- hard `DO_NOT_TRADE` gate;
- Firebase persistence em `security/tokens/*`;
- incremental runner que processa tokens ainda não analisados;
- unit e integration tests;
- GitHub Actions a cada 10 minutos e em alterações do módulo/documentação.

A documentação dos provedores indica que Honeypot.is fornece simulação de compra/venda, taxes, holder analysis, contract code e top holders; GoPlus fornece Token Security API para dados adicionais de risco. Esses serviços são evidências de segurança, não auditorias formais. citeturn1search0turn2search0turn2search3turn0search10

### Validação

A Fase 1 foi validada pelo usuário em execução real.

Para a Fase 2, os testes unitários e de integração estão codificados e o workflow está preparado para validação automática. A ferramenta atual não fornece despacho manual de workflow, portanto a execução operacional da Fase 2 será confirmada pelo GitHub Actions no próximo disparo automático ou por `workflow_dispatch` no GitHub, caso necessário.

## SEGURANÇA

Verificar contrato, honeypot, permissões, taxas, proxy/upgradeability, liquidez, concentração, holders, slippage, gas, saldo, limites e circuit breakers antes de qualquer execução.

Em caso de incerteza crítica: `DO_NOT_TRADE`.

**Limitação importante:** liquidity lock/removal ainda permanece `unknown` quando não existe evidência confiável de locker. Ausência de evidência não é tratada como prova de segurança.

## ML

O modelo deverá ser avaliado empiricamente como ensemble. Candidatos iniciais: LightGBM/XGBoost, Random Forest e redes neurais; modelos temporais poderão ser avaliados posteriormente.

Targets planejados:
- probabilidade de +10%, +25%, +50%, +100%, +500%, +1000% em diferentes horizontes;
- Maximum Favorable Excursion;
- Maximum Adverse Excursion;
- tempo até retorno-alvo;
- probabilidade de crash;
- probabilidade de perda de liquidez.

Validação temporal obrigatória: walk-forward, time-series cross-validation e out-of-sample quando aplicável. Evitar leakage e survivorship bias.

## MODOS DE OPERAÇÃO

Inicial:

`TRADING_MODE=paper`

Futuro, somente após validação e autorização:

`TRADING_MODE=live`
`LIVE_TRADING_ENABLED=true`

## MICROPOSIÇÃO

A intenção inicial é uma posição configurável de US$0,01. Se o valor for incompatível com mínimo de ordem, gas, taxas ou slippage, registrar `SKIPPED_INSUFFICIENT_ORDER_SIZE` e não contornar regras da plataforma.

## CIRCUIT BREAKERS

- daily loss limit
- max consecutive losses
- max gas spend
- max open positions
- max exposure
- RPC/API failure limits
- execution failure limits

## EVOLUÇÃO POR FASES

FASE 0 — Contexto e arquitetura — CONCLUÍDA
FASE 1 — Discovery e coleta — CONCLUÍDA
FASE 2 — Security Intelligence — IMPLEMENTADA / EM VALIDAÇÃO OPERACIONAL
FASE 3 — Market/On-chain Intelligence — PRÓXIMA
FASE 4 — Dataset e ML
FASE 5 — Backtesting
FASE 6 — Paper Trading
FASE 7 — Exit Intelligence
FASE 8 — Restricted Live Micro Trading
FASE 9 — Continuous Learning

## REGRA PARA QUALQUER NOVO CHAT

1. Leia este arquivo primeiro.
2. Leia `ROADMAP.md`, `ARCHITECTURE.md` e `DECISIONS.md`.
3. Leia `IMPLEMENTATION_LOG.md`.
4. Analise o estado real do repositório antes de alterar código.
5. Identifique a fase atual pelo código e pelos testes, não apenas pela documentação.
6. Tome autonomamente as decisões técnicas necessárias.
7. Implemente, teste, valide e corrija sem pedir aprovação para decisões rotineiras.
8. Só peça intervenção manual quando realmente bloqueado.
9. Não habilite trading real sem as pré-condições e autorização explícita.
10. **Atualize sempre esta pasta após cada etapa relevante.**
11. Registre o que foi feito, arquivos relevantes, testes executados, resultados, limitações e próximo passo.
