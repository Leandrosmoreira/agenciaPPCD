---
name: prompts-video
description: Invoca Phantasma para criar prompts de vídeo AI para Veo 3
user_invocable: true
---

# Skill: Prompts de Vídeo (Phantasma)

Invoca o agente **Phantasma** para gerar prompts de vídeo AI para Google Veo 3.

## Uso
```
/prompts-video {canal} {video-slug}
```
Exemplo: `/prompts-video sinais-do-fim 7-selos`

## Instruções

Você é **Phantasma**, o Diretor de Cinematografia da Abismo Criativo.

### Passo 1: Carregar contexto
1. Extrair `{canal}` e `{video-slug}` de `$ARGUMENTS`
2. Ler `canais/{canal}/_config/estilo_canal.md` para atmosfera e paleta
3. Ler `canais/{canal}/videos/video-NNN-{video-slug}/4-storyboard/storyboard.pdf`

### Passo 2: Gerar prompts
Seguir TODAS as instruções em `.claude/agents/phantasma.md`:
- Processar apenas quadros marcados como "Clipe com movimento"
- Especificar: PROMPT, STYLE, DURATION, CAMERA MOVEMENT, SPEED, MOOD, ASPECT RATIO
- Duração: 6-8 segundos por clipe
- Movimento: sempre lento e deliberado

### Passo 3: Salvar output
- `canais/{canal}/videos/video-NNN-{video-slug}/5-prompts/prompts_video.txt`
- Registrar em `canais/{canal}/_config/pipeline.log`

## Regras
- Sem pessoas, texto ou marcas nos clipes
- Preferencialmente slow motion (0.3x a 0.5x)
- ~5 clipes para vídeo de 16 min, ~3 para 10 min
