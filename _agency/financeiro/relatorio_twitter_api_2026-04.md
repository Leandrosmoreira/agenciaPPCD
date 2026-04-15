# Relatório Twitter API v2 — Análise de Custos
**MIDAS — Analista Financeiro | Abismo Criativo**
Data: 09/04/2026 | Ciclo: Apr 5 – May 5, 2026

---

## Situação Atual

| Item | Valor |
|------|-------|
| Pago em 09/04/2026 | $5.00 USD (Mastercard) |
| Gasto acumulado (ciclo) | $0.38 |
| Saldo restante | $4.62 |
| Dias restantes no ciclo | 27 |
| Posts lidos | 76 |
| Requests feitos | 10 |
| Taxa unitária | ~$0.005/post |
| Auto Recharge | DESATIVADO |
| Spend Cap | ILIMITADO |

---

## 1. Custo por Busca e por Vídeo (Argos)

| Métrica | Cálculo | Valor |
|---------|---------|-------|
| Posts por busca | 10 tweets/request | 10 posts |
| Custo por busca | 10 × $0.005 | **$0.05** |
| Buscas por vídeo | 5 buscas (trending topics + confirmação) | 5 buscas |
| Custo Argos/vídeo | 5 × $0.05 | **$0.25** |

---

## 2. Projeção Mensal

| Cenário | Vídeos/mês | Buscas/mês | Custo/mês |
|---------|-----------|-----------|-----------|
| Conservador | 4 vídeos | 20 buscas | **$1.00** |
| Agressivo | 8 vídeos | 40 buscas | **$2.00** |

*Nota: Inclui margem de ~10% para buscas extras/retentativas.*

---

## 3. Duração dos $5.00

Saldo efetivo disponível após gasto atual: **$4.62**

| Cenário | Custo/mês | Meses com $4.62 | Meses com $5.00 completo |
|---------|-----------|----------------|--------------------------|
| 4 vídeos/mês | $1.00 | **~4,6 meses** | ~5 meses |
| 8 vídeos/mês | $2.00 | **~2,3 meses** | ~2,5 meses |

*Ciclo atual (Apr 5 – May 5): gasto de $0.38 = 10 requests de teste. Com uso real de 4 vídeos/mês, o saldo restante de $4.62 cobre mais 4 ciclos completos.*

---

## 4. Alerta: Spend Cap Ilimitado

**Risco: BAIXO — mas recomenda-se configurar cap.**

Motivo: O modelo Pay Per Use ($0.005/post) é barato por natureza. Porém:

- Um bug ou loop no Argos pode disparar centenas de requests sem controle
- Auto Recharge está desativado (bom), mas sem cap a cobrança segue até o saldo acabar e além, dependendo da configuração da conta X
- Com Spend Cap ilimitado, um acidente com 1.000 requests = $50 debitados sem aviso prévio
- Sem notificação automática de limite, o risco é invisível

**Classificação do risco:** Baixo em uso normal, Alto em caso de falha de script.

---

## 5. Recomendação: Spend Cap

**Configurar Spend Cap de $3.00/ciclo.**

Justificativa:
- Cenário 8 vídeos/mês (máximo esperado) = $2.00/mês
- $3.00 oferece 50% de margem de segurança
- Evita cobranças acidentais sem impactar operação real
- Recarregar manualmente quando necessário ($5 cobre 2,5 meses no cenário máximo)

| Opção | Cap | Cobre | Margem |
|-------|-----|-------|--------|
| Conservadora | $2.50 | até 8 vídeos + 25% extra | baixa |
| **Recomendada** | **$3.00** | **até 8 vídeos + 50% extra** | **adequada** |
| Folgada | $5.00 | ciclo completo pago | nenhuma proteção real |

---

## Integração com Custos Gerais

Custo Twitter API por vídeo: **$0.25** (~R$1,37 na cotação atual ~R$5,50/USD)

Impacto no custo total por vídeo (de R$48,72):
- Adiciona **R$1,37/vídeo** → novo total: **R$50,09/vídeo**
- Impacto: +2,8% — desprezível na estrutura de custos atual

---

## Ações Recomendadas

- [ ] Configurar Spend Cap de $3.00 no painel X Developer
- [ ] Ativar notificação de uso (email) quando atingir 80% do cap
- [ ] Manter Auto Recharge DESATIVADO
- [ ] Registrar Twitter API em `custos_ferramentas.md` como custo variável
- [ ] Próxima recarga manual: quando saldo < $1.00 (repor $5.00)

---

*Gerado por MIDAS — Analista Financeiro da Abismo Criativo*
*[2026-04-09] Dados baseados em ciclo real Apr 5 – May 5, 2026*
