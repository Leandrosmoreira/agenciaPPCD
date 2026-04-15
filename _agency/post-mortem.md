# Post-Mortem Log — Abismo Criativo

> Registro de lições aprendidas por vídeo publicado.
> Regra dos 3x: se um erro se repetiu 3 vezes → escalar para ADR + CLAUDE.md.

---

## PM-001: sinais-do-fim/video-001-armagedom (2026-04-06)
**Resultado:** retenção 42% | CTR 6.1% | views 320 (48h) | tempo 5:20 min
**O que funcionou:** CTR acima de 5% (thumbnail com rosto real chorando). Tema evergreen.
**O que falhou:** Retenção 42% (meta >55%). Intro de 15s com saudação matou o hook. Duração 15:30 (excesso).
**Lição:** Primeiros 10s = gancho agressivo. Zero saudação. Roteiro mais curto.
**Ação tomada:** ADR-003 (10-12 min) + ADR-007 (gancho sem saudação)
**Recorrente?** 1ª vez

## PM-002: sinais-do-fim/video-002-marca-da-besta (2026-04-08)
**Resultado:** retenção 48% | CTR 5.8% | views 410 (48h) | tempo 6:10 min
**O que funcionou:** Melhoria de retenção (+6pp vs video-001). Hook mais direto.
**O que falhou:** Retenção ainda abaixo de 55%. Duração 15:30 novamente. Repetição temática entre atos.
**Lição:** Cada ato deve cobrir UM ângulo único. Revisão obrigatória anti-repetição.
**Ação tomada:** Regra no estilo_canal.md (máx 13-14 min, checar repetição)
**Recorrente?** 2ª vez (retenção abaixo da meta) — ALERTA

---

## Padrões Rastreados

| Padrão | Ocorrências | Status |
|--------|-------------|--------|
| Retenção <55% | 2x (video-001, video-002) | ALERTA — próxima vez escalar para ADR |
| Duração >14 min | 2x (video-001, video-002) | RESOLVIDO — ADR-003 (10-12 min) |
| Hook fraco (saudação) | 1x (video-001) | RESOLVIDO — ADR-007 |
