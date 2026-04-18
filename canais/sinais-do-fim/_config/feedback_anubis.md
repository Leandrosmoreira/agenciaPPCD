# FEEDBACK ANUBIS → AGENTES
**Canal:** Sinais do Fim
**Última atualização:** 2026-04-16
**Fonte:** analytics_completo_2026-04-16.json (181 views | 5 vídeos | 8 inscritos)

> Este arquivo é atualizado por Anubis após cada ciclo de coleta.
> **TODOS os agentes DEVEM ler este arquivo antes de executar suas tarefas.**

---

## 🏆 TEMPLATE VALIDADO: ARMAGEDOM

O vídeo `video-001-armagedom` é o único que gerou inscrições (8 em 9 dias) e manteve retenção acima de 50% consistentemente.

**Padrões a replicar:**
- Roteiro usa fatos verificáveis + urgência + conexão bíblica direta
- Hook de 10s ancorado em evento real (não em abstração teológica)
- Retenção dia 07: 53% | dia 09: **73%** | dia 11: 50%
- Tráfego via RELATED_VIDEO (52%) + YT_SEARCH (12%) — algoritmo orgânico

---

## MORRIGAN — Lições para Roteiro

### ✅ FAZER
1. **Inserir 2 perguntas diretas** por roteiro — uma no meio, uma no fim. Exemplos:
   - "O que você acha disso? Me conta nos comentários."
   - "Você já notou esse padrão? Comenta aí o que pensa."
   (Meta: sair de 1.1% para 3%+ de comment rate)
2. **Entregar a promessa do título nos primeiros 90s** — qualquer "curiosity gap" do título deve ter sua resposta prometida até 1:30
3. **Estrutura Armagedom:** fato verificável (30s) → contexto bíblico (2min) → aprofundamento (7min) → conexão presente (2min) → CTA + pergunta (1min)
4. **Cauda longa funciona:** inscrições aparecem até 7 dias depois se a retenção for alta. Prioridade = retenção > views imediatas

### ❌ EVITAR
1. **Nome de celebridade em título quando roteiro for teológico** — Trump/Kushner/Musk atraem público que não quer teologia. Retenção Trump: **15% (falha)**.
2. **Abertura didática lenta** — "Nos dias de hoje..." ou "A Bíblia diz que..." nos primeiros 10s = abandono imediato.
3. **Roteiros que prometem "revelação" mas entregam análise** — inconsistência título→conteúdo = retenção em queda livre.

---

## HERMES — Lições para SEO + Títulos

### ✅ FAZER
1. **Keywords de busca ativa no nicho:** usar termos que têm YT_SEARCH real
   - Funcionam: "Armagedom", "Marca da Besta", "Anticristo", "Apocalipse"
   - Verificar: "UAP 2025", "disclosure pentágono", "Claude AI profecia"
2. **Título = promessa que o roteiro DEVE cumprir nos primeiros 90s**
3. **Títulos curtos + keyword posição 1** performaram melhor que títulos longos descritivos

### ❌ EVITAR
1. **Celebridade no título** sem roteiro 100% focado nela (Trump: 49 views, 0 inscritos, 15% retenção)
2. **Títulos com "HOJE" ou "AGORA"** sem evento verificável real para ancorar — público percebe clickbait em 30s

---

## MEDUSA — Lições para Thumbnails

### ✅ FAZER
1. **Mobile-first SEMPRE:** 75-87% das views vêm de mobile. Texto legível em tela de 5"
   - Fonte mínima: ocupa >8% da altura da thumbnail
   - Contraste extremo: texto branco/amarelo sobre fundo escuro
2. **TV-ready (crescendo):** Armagedom teve 30% de views em TV (Chromecast/SmartTV)
   - Thumbnail deve ser impactante em tela grande também
   - Nada de detalhes finos que somem em TV de 50"
3. **Testar preview mobile no YouTube Studio** antes de aprovar — obrigatório

### ❌ EVITAR
1. Texto pequeno ou detalhado que some em mobile
2. Cores similares entre texto e fundo (baixo contraste)

---

## SIBILA — Lições para Metadata + Publicação

### ✅ FAZER
1. **EXT_URL é audiência premium:** views via URL externa têm 8.75 min/view (vs 2-3 min/view orgânico). Isso impacta o algoritmo positivamente.
2. **Divulgação via WhatsApp/X no dia do lançamento:** coordenar com Snayder para disparar links em grupos no dia D
3. **Chapters nos primeiros vídeos** são obrigatórios — ajudam retenção ao sinalizar estrutura para o espectador
4. **Descrição com perguntas** para estimular comentários orgânicos

### ❌ EVITAR
1. Publicar sem coordenar divulgação externa — Marca da Besta teve 4 views externas com 35 min total = mais impacto por view que qualquer outra fonte

---

## ARGOS — Lições para Pesquisa de Temas

### ✅ FAZER
1. **Temas com busca orgânica ativa:** Armagedom foi o ÚNICO com YT_SEARCH relevante (7 views). Priorizar temas que as pessoas realmente buscam
2. **Correlação evento real + passagem bíblica específica** = melhor retenção. Abstrato = abandono.
3. **Temas com "janela de urgência"** (evento recente + conexão bíblica) → divulgação externa natural

### ❌ EVITAR
1. Temas que só têm curiosidade (clique) mas não entregam substância verificável
2. Temas sobrepostos com concorrentes sem ângulo diferenciador claro

---

## ANUBIS — Regras de Coleta e Alerta

### Coleta automática
- **Cron:** todo dia 20:57 → `python _tools/anubis_analytics_api.py`
- **Saída:** `analytics_completo_YYYY-MM-DD.json` + `_agency/analytics/daily_summary_YYYY-MM-DD.md`
- **Post-mortem semanal:** domingo 21:37

### Alertas automáticos (verificar no summary diário)
- 🔴 **CRÍTICO:** retenção média < 20% no dia 1 → notificar Snayder + revisar título/gancho
- 🟡 **ATENÇÃO:** nenhum inscrito em 48h pós-lançamento → revisar CTA no roteiro
- 🟢 **POSITIVO:** retenção > 50% em qualquer dia → registrar padrão + notificar Morrigan

### Após cada coleta
1. Atualizar este arquivo `feedback_anubis.md` com novos dados
2. Identificar se algum vídeo novo entrou no padrão "Armagedom" (conversor)
3. Reportar para Azrael (orquestrador)

---

## 📈 BENCHMARKS DO CANAL (base: 5 vídeos, 181 views)

| Métrica | Atual | Meta (30 vídeos) |
|---------|-------|-----------------|
| Retenção média | 35% | >50% |
| Like rate | 21% | >10% (já acima!) |
| Comment rate | 1.1% | >3% |
| Inscrito/vídeo | 1.6 | >10 |
| Views/dia pós-lançamento | 8 | >50 |
| % tráfego YT_SEARCH | 4% | >20% |

**Nota:** like rate de 21% é EXCELENTE para qualquer canal. O problema é retenção e comentários.

---

*Próxima revisão: 2026-04-17 após coleta diária*
