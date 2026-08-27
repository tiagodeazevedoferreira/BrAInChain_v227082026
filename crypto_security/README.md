# Crypto Security Intelligence

Fase 2 do Autonomous Crypto Launch Intelligence & Trading.

## Objetivo

Transformar cada `DiscoveredPool` da Fase 1 em um `SecurityAnalysis` auditável e persistido em Firebase. A segurança é um hard gate: `DO_NOT_TRADE` por padrão e nunca há execução de compra nesta fase.

## Camadas

1. **Honeypot simulation** — Honeypot.is: honeypot status, buy/sell/transfer taxes, simulation success, holder sell failures/siphoning, source/proxy indicators.
2. **Contract verification** — Honeypot.is: root/external contract source status and proxy calls.
3. **Top holders** — Honeypot.is: top 50 holders; calcula concentração do top holder e top 5.
4. **Optional GoPlus** — se `GOPLUS_ACCESS_TOKEN` existir, adiciona token security data como segunda fonte.
5. **Local deterministic scoring** — consolida evidências em `risk_score`, `risk_level`, flags críticas, warnings e `trade_gate`.
6. **Firebase** — grava em `security/tokens/*` e `security/status`.

Honeypot.is documenta o endpoint `/v2/IsHoneypot` para simulação/honeypot, o endpoint `/v2/GetContractVerification` para verificação do contrato e `/v1/TopHolders` para os 50 maiores holders. citeturn1search0turn2search0turn2search3

GoPlus possui Token Security API para análise de segurança de tokens e suporte a várias chains/DEXs; o adapter é opcional para não bloquear a fase quando nenhuma credencial GoPlus estiver configurada. citeturn0search8turn0search10turn0search5

## Hard gates

- honeypot detectado → `DO_NOT_TRADE`
- falha crítica de venda → `DO_NOT_TRADE`
- concentração extrema → `DO_NOT_TRADE`
- código fechado/estado crítico desconhecido → risco elevado e bloqueio conforme score
- segurança desconhecida → `DO_NOT_TRADE`
- liquidez muito baixa → bloqueio
- liquidity lock não conhecido → warning e risco adicional

## Limitações

- Não existe detector perfeito de rug pull/honeypot.
- APIs de segurança podem estar indisponíveis, atrasadas ou sem suporte à chain.
- Liquidity lock/removal ainda é tratado como estado `unknown` quando não há evidência de locker; não será inferido como seguro.
- A análise não é auditoria formal de smart contract.
- Live trading permanece desabilitado.
