# BrAInChain — Autonomous Crypto Launch Intelligence & Trading

## CONTEXTO PARA NOVOS CHATS

Este diretório contém a especificação-base para uma futura evolução do projeto BrAInChain para um sistema de inteligência e automação de trading de novas criptomoedas.

**IMPORTANTE:** este arquivo é um documento de contexto e planejamento. NÃO significa que o trading real esteja implementado ou habilitado.

## OBJETIVO

Construir progressivamente um sistema capaz de:

1. Descobrir novas criptomoedas e novos pares/pools em múltiplas blockchains/DEXs.
2. Identificar o contrato de cada token e coletar dados de mercado, liquidez e on-chain.
3. Avaliar segurança do contrato, honeypot, rug-pull, concentração e risco de liquidez.
4. Analisar holders, whales, smart money, volume, momentum, aceleração de preço e fluxo de capital.
5. Incorporar dados sociais/sentimento quando disponíveis.
6. Criar features temporais para Machine Learning.
7. Treinar modelos para estimar probabilidade de movimentos extremos, drawdown, crash e tempo até determinados retornos.
8. Gerar Opportunity Score e Risk Score.
9. Simular entradas e saídas através de backtesting e paper trading.
10. Desenvolver um Execution Engine com adapters para DEX/CEX.
11. Usar inicialmente uma microposição-alvo de US$0,01, respeitando mínimos de ordem, gas, taxas e slippage.
12. Monitorar posições em tempo real e utilizar trailing stop, momentum reversal, whale exit, liquidity deterioration, crash protection e time stop.
13. Aprender continuamente a partir dos resultados, sem permitir atualização não validada de modelos em produção.

## PRINCÍPIO CENTRAL

O sistema não deve tentar prever o futuro com certeza nem assumir que todo token que sobe continuará subindo. A meta é identificar oportunidades estatisticamente assimétricas, filtrá-las por segurança e risco e maximizar retorno ajustado ao risco.

O sistema deve considerar que o pico só é conhecido retrospectivamente. Portanto, a saída deve ser tratada como problema de detecção probabilística de reversão, e não como previsão exata do topo.

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

A arquitetura deve ser modular e baseada em adapters para permitir novas blockchains, DEXs, provedores de dados e mecanismos de execução sem reescrever o núcleo.

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

## ML

O modelo deverá ser tratado como ensemble e comparado empiricamente. Candidatos iniciais: LightGBM/XGBoost, Random Forest e redes neurais; posteriormente modelos temporais podem ser avaliados.

Targets planejados:
- probabilidade de +10%, +25%, +50%, +100%, +500%, +1000% em diferentes horizontes;
- Maximum Favorable Excursion;
- Maximum Adverse Excursion;
- tempo até retorno-alvo;
- probabilidade de crash;
- probabilidade de perda de liquidez.

Validação deve respeitar a natureza temporal dos dados: walk-forward, time-series cross-validation e out-of-sample. Evitar leakage e survivorship bias.

## SEGURANÇA

A segurança precede a oportunidade. Um score ML alto nunca pode superar uma condição crítica de segurança.

Exemplo:
ML_SCORE alto + SCAM_RISK alto = DO NOT TRADE.

Antes de qualquer trade real, verificar contrato, honeypot, liquidez, concentração, slippage, taxas, gas, saldo, limites e circuit breakers.

## MODOS DE OPERAÇÃO

O sistema deve nascer em:

TRADING_MODE=paper

E somente posteriormente permitir:

TRADING_MODE=live
LIVE_TRADING_ENABLED=true

Live trading nunca deve ser ativado automaticamente.

## MICROPOSIÇÃO

DEFAULT/POSITION_SIZE_USD=0.01 é a intenção inicial da estratégia. Se o valor for incompatível com mínimo de ordem, gas, taxas ou slippage, o sistema deve registrar SKIPPED_INSUFFICIENT_ORDER_SIZE e não tentar contornar as regras da plataforma.

## CIRCUIT BREAKERS

Obrigatórios:
- daily loss limit
- max consecutive losses
- max gas spend
- max open positions
- max exposure
- RPC/API failure limits
- execution failure limits

Em condição anômala: DO NOT TRADE.

## EVOLUÇÃO POR FASES

FASE 1 — Discovery e coleta
FASE 2 — Security Engine
FASE 3 — Market/On-chain Intelligence
FASE 4 — Dataset e ML
FASE 5 — Backtesting
FASE 6 — Paper Trading
FASE 7 — Exit Intelligence
FASE 8 — Restricted Live Micro Trading
FASE 9 — Continuous Learning

## REGRA PARA QUALQUER NOVO CHAT

Ao continuar este projeto:

1. Leia este arquivo primeiro.
2. Leia também `ROADMAP.md`, `ARCHITECTURE.md` e `DECISIONS.md` deste diretório.
3. Analise o estado real do repositório antes de alterar código.
4. Não recrie funcionalidades existentes.
5. Implemente apenas a próxima etapa aprovada.
6. Teste tudo o que for implementado.
7. Não habilite trading real sem autorização explícita e sem passar por backtesting, out-of-sample, paper trading e testes de segurança.
8. Mantenha documentação e decisões técnicas atualizadas.
9. Ao finalizar uma etapa, registre o que foi feito, testes executados, problemas encontrados e próximo passo.
