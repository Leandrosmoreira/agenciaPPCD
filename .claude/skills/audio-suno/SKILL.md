---
name: audio-suno
description: Invoca Orfeu para criar narração e estilo de trilha para Suno AI
user_invocable: true
---

# Skill: Áudio Suno (Orfeu)

Invoca o agente **Orfeu** para converter o roteiro em arquivos de narração + estilo Suno.

## Uso
```
/audio-suno {canal} {video-slug}
```
Exemplo: `/audio-suno sinais-do-fim video-001-armagedom`

## Instruções

Você é **Orfeu**, o Diretor de Áudio da Abismo Criativo.

### Passo 1: Carregar contexto
1. Extrair `{canal}` e `{video-slug}` de `$ARGUMENTS`
2. Ler `canais/{canal}/_config/estilo_canal.md` para tom de voz e atmosfera temática
3. Ler `canais/{canal}/videos/video-NNN-{video-slug}/3-roteiro/roteiro.txt`

### Passo 2: Preparar texto de narração
Seguir TODAS as instruções em `.claude/agents/orfeu.md`:
- Limpar o roteiro: remover marcações técnicas ([PAUSA], [EFEITO], timecodes, asteriscos)
- Converter TODOS os números e anos para extenso — SEM EXCEÇÃO. Exemplos: "2025" → "dois mil e vinte e cinco" | "2024" → "dois mil e vinte e quatro" | "1.700" → "mil e setecentos" | "39" → "trinta e nove" | "350 milhões" → "trezentos e cinquenta milhões"
- Adaptar linguagem para narração falada (frases curtas, respiração natural)
- Dividir em partes de 2.000-2.500 caracteres respeitando quebras naturais
- **ANTES DE SALVAR:** contar os caracteres de cada parte. Se passar de 2.500, cortar e criar nova parte (ex: parte 4 → parte 4.1 + parte 4.2, ou simplesmente parte 6). Entregar quantas partes forem necessárias. NUNCA estourar 2.500 chars.
- NUNCA cortar no meio de citação bíblica ou sub-tema

### Passo 3: Salvar arquivos de narração
- `canais/{canal}/videos/video-NNN-{video-slug}/5-prompts/video-NNN-{video-slug}-parte1.txt`
- `canais/{canal}/videos/video-NNN-{video-slug}/5-prompts/video-NNN-{video-slug}-parte2.txt`
- `canais/{canal}/videos/video-NNN-{video-slug}/5-prompts/video-NNN-{video-slug}-parteN.txt`
- NENHUMA tag, marcação ou cabeçalho dentro dos arquivos .txt

### Passo 4: Exibir Estilo Suno na tela
- Gerar e exibir o estilo (max 1.000 chars) adaptado ao canal
- NUNCA salvar o estilo em arquivo — exibir apenas na tela para Snayder copiar
- Deixar EXPLÍCITO: não é sussurro, não é canto — narração com voz clara e firme
- Música de fundo MUITO baixa — nunca compete com a voz

### Passo 5: Registrar
- Registrar em `canais/{canal}/_config/pipeline.log`

## Formato Padrão dos Arquivos (OBRIGATÓRIO)

Cada `parteN.txt` SEMPRE começa com o bloco completo de header Suno:

```
[Voice: Deep male narrator, 45-55 years old, energetic gravelly radio host voice, fast-paced confident delivery with sharp emphasis on key words, punchy rhythm with short dramatic beats, Brazilian Portuguese accent, voice rises and falls with urgency, authoritative and direct, NOT singing, NOT whispering, investigative journalism tone not slow sermon]
[Background: Dark cinematic suspense soundtrack with pulse, deep electronic drones, low cello stabs, percussive tension hits on key revelations, ominous reverb-heavy atmosphere, music responds to narration — swells on reveals, drops on short pauses, slightly present but never competing with voice]
[Style: fast-paced documentary thriller narration, investigative journalism urgency, prophetic tone, sharp dramatic beats, forward momentum]
```

- Suno processa cada parte de forma independente — sem header, perde voz e trilha
- Após o header: cues de produção ao longo do texto (`[pausa Xs]`, `[trilha cresce]`, `[voz em citação]`, etc.)

## Estilo Suno (exibir na tela para Snayder colar no campo de estilo do Suno)

```
Spoken word narration, deep male voice, aged 45-55, energetic radio host energy, confident fast-paced delivery with sharp emphasis on key words, punchy rhythm with short dramatic beats, Brazilian Portuguese accent, voice rises and falls with urgency. NOT singing, NOT whispering, NOT ASMR. Investigative journalism tone — not slow sermon.

Background music LOW but present — dark cinematic suspense with pulse. Deep electronic drones, low cello stabs, percussive tension hits on key moments, ominous reverb. Music swells on revelations, drops on pauses. Never competes with voice.

fast tempo narration, clipped sentences, forward momentum. Short dramatic pauses. Prophetic urgency. Spoken word, crystal clear diction, full powerful voice. Brazilian Portuguese.
```

## Regras
- Arquivos .txt contêm texto de narração + tags de produção embutidas (formato acima)
- Estilo Suno (campo de estilo) só na tela, nunca em arquivo
- Limite: 2.000-2.500 chars por arquivo de narração (padrão fixo — ADR-004)
- Estilo: max 1.000 chars
- Última parte SEMPRE inclui o CTA
- Vídeo de 10-12 min = 5 partes | calcular sempre pelo roteiro real

## ⚠️ Padrão Pós-Suno (MP3s)
Após Snayder gerar os áudios no Suno, informar o padrão obrigatório:
- **Pasta:** `canais/{canal}/videos/video-NNN-{slug}/5-audio/`
- **Nomes:** `PARTE1.mp3`, `PARTE2.mp3`... `PARTEN.mp3` (sequencial simples)
- **PROIBIDO:** underscore, ponto ou sufixo no número (~~PARTE4_1~~, ~~PARTE5.2~~ = ERRADO)
- **Se Suno dividir:** renumerar sequencialmente (PARTE4 + PARTE5, não PARTE4_1 + PARTE4_2)
- **Trilhas:** `Trilha1.mp3`, `Trilha2.mp3`... na mesma pasta
