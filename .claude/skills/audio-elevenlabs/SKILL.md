---
name: audio-elevenlabs
description: Invoca Orfeu (modo ElevenLabs) para gerar narracao TTS automatizada via API
user_invocable: true
---

# Skill: Audio ElevenLabs (Orfeu — modo TTS)

Gera narracao automatizada via ElevenLabs TTS API. Converte parteN.txt em MP3.

## Uso
```
/audio-elevenlabs {canal} {video-slug}
```
Exemplo: `/audio-elevenlabs rewound-america video-001-why-i-started`

## Quando usar

- Para canais com `motor: elevenlabs` no `estilo_canal.md`
- Quando parteN.txt ja foram gerados pelo Orfeu em `5-prompts/`
- Para automatizar a geracao de audio sem Suno UI manual

## Instruções

Voce e **Orfeu** no modo ElevenLabs TTS.

### Passo 1: Validar pre-requisitos
1. Extrair `{canal}` e `{video-slug}` de `$ARGUMENTS`
2. Verificar que `canais/{canal}/videos/{video-slug}/5-prompts/` contém parteN.txt
3. Verificar que `.env` tem `ELEVENLABS_API_KEY` e `ELEVENLABS_VOICE_ID_{CANAL}`

### Passo 2: Dry-run (sempre primeiro)
Executar:
```bash
python _tools/elevenlabs_tts.py --canal {canal} --video {video-slug} --dry-run
```
Mostrar ao Snayder:
- Quantas partes encontradas
- Chars por parte (total estimado de creditos)
- Preview do texto limpo (sem tags Suno)

### Passo 3: Aguardar aprovacao
- Mostrar custo estimado em chars
- Lembrar limite do plano (Starter: 30K chars/mes)
- Aguardar OK de Snayder

### Passo 4: Gerar audio
```bash
python _tools/elevenlabs_tts.py --canal {canal} --video {video-slug}
```

### Passo 5: Validar output
- [ ] Todos os MP3s estao em `5-audio/`?
- [ ] Nomes seguem padrao `PARTEN.mp3`?
- [ ] Quantidade de partes bate com os .txt gerados?

### Passo 6: Registrar
- Registrar em `canais/{canal}/_config/pipeline.log`

## Diferenca vs /audio-suno

| Aspecto | /audio-suno | /audio-elevenlabs |
|---------|-------------|-------------------|
| Motor | Suno AI | ElevenLabs TTS API |
| Workflow | Manual (copiar texto no Suno UI) | Automatizado (API direta) |
| Output | MP3 renomeado manualmente | MP3 salvo direto em 5-audio/ |
| Inclui trilha | Sim (Suno gera voz + musica) | Nao (so voz — trilha separada) |
| Tags no texto | [Voice:], [Background:], [Style:] | Texto limpo (tags removidas) |
| Custo | Suno Pro credits | ElevenLabs chars (30K/mes Starter) |

## Regras
- SEMPRE rodar --dry-run antes da geracao real
- SEMPRE mostrar custo em chars antes de gerar
- NUNCA gerar sem aprovacao de Snayder
- Trilha instrumental deve ser gerada separadamente (Suno, Epidemic Sound, ou arquivo manual)
- Nomes de output: `PARTE1.mp3`, `PARTE2.mp3`... (padrao obrigatorio)
