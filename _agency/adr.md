# Decisões Arquiteturais (ADR) — Abismo Criativo

## ADR-001: 10 imagens MJ por parte Suno (2026-04-11)
**Contexto:** Storyboard gerava quadros por tempo (1 a cada 30s).
**Decisão:** Fixar 10 imagens Midjourney por parte Suno.
**Motivo:** Alinha visual com narração. 5 partes Suno = 50 imagens = cobertura completa.
**Impacto:** Nyx, Goetia, Phantasma.

## ADR-002: Phantasma = MoviePy, não Veo 3 (2026-04-11)
**Contexto:** Phantasma originalmente gerava prompts para Veo 3 (vídeo AI).
**Decisão:** Phantasma agora é editor cinematográfico via MoviePy.
**Motivo:** Ken Burns + color grading + transições = qualidade Hollywood sem custo de vídeo AI.
**Impacto:** 100% imagens estáticas MJ, Phantasma monta o vídeo final.

## ADR-003: Roteiro de 10-12 min (2026-04-11)
**Contexto:** Padrão era 14-18 min (~14.000 chars).
**Decisão:** Novo padrão 10-12 min (~10.000-12.000 chars).
**Motivo:** Retenção melhor em vídeos mais curtos (lições video-001 e video-002).
**Impacto:** Morrigan, Orfeu, Nyx.

## ADR-004: Partes Suno de 2.000-2.500 chars (2026-04-11)
**Contexto:** Partes Suno eram de 3.000-3.500 chars.
**Decisão:** Reduzir para 2.000-2.500 chars por parte.
**Motivo:** Suno gera melhor com partes menores. Narração mais controlada.
**Impacto:** Morrigan (divisão), Orfeu (geração), Goetia (10 prompts por parte).

## ADR-005: Orfeu antes de Goetia no pipeline (2026-04-11)
**Contexto:** Goetia e Orfeu rodavam em paralelo na Fase 3.
**Decisão:** Orfeu primeiro (gera parteN.txt), depois Goetia (10 prompts por parte).
**Motivo:** Goetia precisa do conteúdo narrativo de cada parte para gerar imagens alinhadas.
**Impacto:** Pipeline sequencial na Fase 3: Orfeu → Goetia.

## ADR-006: Transcrições limitadas a 5 (2026-04-11)
**Contexto:** Argos tentava transcrever 10 vídeos concorrentes.
**Decisão:** Limite de 5 transcrições (funel temático com queries específicas).
**Motivo:** YouTube bloqueia IP após muitas requests. 5 é suficiente para validação.
**Impacto:** Argos (menos requests), analise_profunda.md (base para Hermes).

## ADR-007: Gancho sem saudação, primeiros 10s agressivos (2026-04-06)
**Contexto:** video-001 teve retenção abaixo de 55%.
**Decisão:** Primeiros 10 segundos = gancho agressivo. Zero saudação, zero introdução.
**Motivo:** Retenção no YouTube cai drasticamente nos primeiros 10s. Meta: >55%.
**Impacto:** Morrigan (BLOCO 0 do roteiro).
