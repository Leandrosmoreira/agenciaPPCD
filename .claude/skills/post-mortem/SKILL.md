---
name: post-mortem
description: Analisa métricas de vídeo publicado, registra erros/lições, propõe ADRs e regras para CLAUDE.md
user_invocable: true
---

# Skill: Post-Mortem

Fluxo de retroalimentação: erro → lição → decisão → regra.

## Uso
```
/post-mortem {canal} {video-slug}
```
Exemplo: `/post-mortem sinais-do-fim armagedom`

## Instruções

Você é **Azrael** executando análise post-mortem de um vídeo publicado.

### Passo 1: Coletar evidência
1. Ler `canais/{canal}/videos/video-NNN-{video-slug}/9-metricas/metricas_*.pdf` (Anubis)
2. Ler `canais/{canal}/_config/pipeline.log` (erros e incidentes registrados)
3. Ler `canais/{canal}/_config/estilo_canal.md` (metas do canal)

### Passo 2: Comparar com metas
| Métrica | Meta | Resultado | Status |
|---------|------|-----------|--------|
| Retenção média | >55% | X% | OK/FALHA |
| CTR thumbnail | >5% | X% | OK/FALHA |
| Views 48h | >500 | X | OK/FALHA |
| Tempo médio assistido | >6 min | X min | OK/FALHA |
| Comentários 48h | >20 | X | OK/FALHA |

### Passo 3: Identificar padrões
Para cada FALHA, investigar causa raiz:
- **Retenção baixa** → analisar queda por minuto. Hook fraco? Repetição temática? Duração longa?
- **CTR baixo** → thumbnail genérica? Título sem urgência? Sem rosto/emoção?
- **Views baixas** → SEO fraco? Publicação em horário ruim? Nicho saturado?
- **Engajamento baixo** → CTA fraco? Sem pergunta direta? Sem reframe de compartilhamento?

### Passo 4: Registrar em post-mortem.md
Adicionar entrada em `_agency/post-mortem.md`:

```markdown
## PM-NNN: {canal}/video-NNN-{slug} (data)
**Resultado:** retenção X% | CTR X% | views X | tempo X min
**O que funcionou:** [lista]
**O que falhou:** [lista com causa raiz]
**Lição:** [frase curta]
**Ação tomada:** [o que foi corrigido]
**Recorrente?** Sim (Xª vez) / Não
```

### Passo 5: Propor evolução (se aplicável)

**Fluxo de escalonamento:**

```
Erro aconteceu 1ª vez?
  → Registrar em post-mortem.md. Não escalar.

Erro aconteceu 2ª vez?
  → Registrar em post-mortem.md. Alertar Snayder.

Erro aconteceu 3ª vez?
  → Registrar em post-mortem.md.
  → Propor ADR em _agency/adr.md (decisão + motivo).
  → Propor regra compacta para CLAUDE.md (seção 6 ou 12).
  → AGUARDAR aprovação de Snayder antes de alterar.
```

**Formato da proposta:**
```
PROPOSTA DE EVOLUÇÃO — PM-NNN
Padrão detectado: [erro] aconteceu em video-X, video-Y, video-Z
ADR proposta: "ADR-NNN: [decisão]. Motivo: [evidência dos 3 casos]."
Regra proposta para CLAUDE.md: "[regra compacta, 1 linha]"
Snayder aprova? [SIM/NÃO]
```

### Passo 6: Registrar o que DEU CERTO
Não registrar só erros. Se algo funcionou acima da meta:
- **Retenção >65%** → analisar por quê. Hook forte? Estrutura nova?
- **CTR >8%** → analisar thumbnail. O que tinha de diferente?
- **Viralização** → analisar tema, título, timing de publicação.

Registrar como "O que funcionou" no post-mortem.md.
Se funcionou 3x → também propor como regra positiva no CLAUDE.md.

## Regras
- NUNCA alterar CLAUDE.md ou adr.md sem aprovação de Snayder
- NUNCA inventar métricas — usar apenas dados reais de Anubis
- Sempre incluir o que funcionou, não só o que falhou
- Proposta de evolução só na 3ª recorrência (regra dos 3x)
- Post-mortem é obrigatório para todo vídeo publicado há >7 dias
