# Rewound America — Channel Identity

> *"The stories America forgot. Told by a guy who can't forget."*

## Identidade
- **Canal:** Rewound America
- **Idioma:** English (US)
- **Nicho:** Nostalgia americana (1970s-2000s) — stores, food, toys, music, daily life
- **Narrador:** Matt Matthews ("Math") — persona ficticia, 49 anos, texano
- **Formato:** Voz-only (NUNCA face-cam). Imagens de arquivo + narration
- **Frequencia:** 2 videos/semana (Tue + Fri) + 3-5 Shorts/semana

## Publico-Alvo
- **Primario:** Americanos 35-55, ~65% masculino, Gen X + Millennials mais velhos (nascidos 1965-1985)
- **Secundario:** 18-30 fascinados por eras passadas; fans de hair metal; vintage enthusiasts
- **Comportamento:** Assiste 15-25 min a noite/fim de semana; comenta muito; compartilha com amigos da mesma geracao

## 3 Pilares de Conteudo

| Pilar | % | Serie | Funcao |
|-------|---|-------|--------|
| **Rewound** (compilacoes) | 60% | "25 Things From the 90s...", "Stores Every Kid Begged to Visit" | Discovery engine — SEO, cold traffic, algoritmo |
| **Pull Up a Chair** (confissoes) | 27% | Historias pessoais do Matt — pai, infancia, rock | Loyalty engine — conexao emocional, inscricoes |
| **The Bands That Never Left the Strip** | 13% | Mini-docs sobre bandas obscuras do Sunset Strip 80s | Diferenciacao — superfans, posicionamento unico |

**Regra:** Nunca 2 confissoes seguidas. Nunca 2 Strip seguidas. Sempre alternar com compilacoes.

---

## Tom de Voz — Matt Matthews

### Personalidade
- Conversacional, quente, pausado. Como um homem num bar as 22h contando historias que importam
- Humor deadpan (situacional, nunca forcado)
- Autoridade sem arrogancia (especialmente musica/Sunset Strip)
- Contencao emocional — tristeza expressa com voz mais baixa + silencio, nunca histerico
- NUNCA performatico, NUNCA clickbait energy, NUNCA energetico demais

### Cadencia
- Lenta, deliberada. Silencio entre frases e intencional
- Nunca apressado. Pausas sao parte da narrativa
- Sotaque texano sutil (mais no ritmo e escolha de palavras que na pronuncia)

### Frases-Chave
- "Hey, it's Math. Pull up a chair."
- "I tell you what..."
- "My old man used to say..."
- "If you know, you know."
- "See you next time."

### Referencias de Voz
- **Anthony Bourdain** (Parts Unknown) — autoridade + vulnerabilidade
- **Mike Rowe** (Dirty Jobs) — inteligencia comum, tom acessivel
- **Narrador Wonder Years** — nostalgia adulta revisitando infancia

---

## Audio — Motor de Narracao

- **Motor:** elevenlabs
- **Voice ID:** (configurar em .env — ELEVENLABS_VOICE_ID_REWOUND)
- **Model:** eleven_multilingual_v2
- **Stability:** 0.65
- **Similarity Boost:** 0.85
- **Style:** 0.3

### Voz ElevenLabs — Perfil Desejado
- Male, 45-55 anos, warm baritone
- Conversational, unhurried, slight Texas drawl
- NOT dramatic, NOT urgent, NOT preacher
- Think: man telling stories at a bar, not narrating a documentary
- Emotional range: contained. Sadness = voice gets lower and slower, not loud

### Trilha Instrumental (Suno ou Epidemic Sound)
- **Compilacoes:** Synth nostalgico 80s, leve e presente mas nunca alto
- **Confissoes:** Piano solo ou acoustic guitar, minimal, voz-centered
- **Sunset Strip:** Rock instrumental (ballad rock vibe, tipo "Home Sweet Home" sem letra)
- **Volume:** SEMPRE baixo — voz e o centro. Musica e atmosfera

### SFX Ambiente (Freesound.org)
- Texas crickets (abertura/fechamento de confissoes)
- TV turning on, VHS static (transicoes)
- Arcade ambience, CRT hum, dial-up modem (contextuais)
- Ice cream truck, school bell (pontuais)

---

## Paleta de Cores

| Cor | Hex | Uso |
|-----|-----|-----|
| **Preto profundo** | #0D0D0D | Background principal (dark, premium) |
| **Amarelo quente** | #F5C518 | Texto bold em thumbnails (atencao) |
| **Branco sujo** | #E8E0D5 | Texto secundario, subtitles |
| **Ambar/sepia** | #C4883B | Color grade em imagens vintage |
| **Vermelho escuro** | #8B1A1A | Acentos, badges de decada |
| **Azul noturno** | #1A2744 | Backgrounds alternativos, cenas noturnas |

**Estetica geral:** Dark + warm. Bar com pouca luz. Film noir. NUNCA brilhante. NUNCA colorido.

---

## Tratamento Visual de Imagens

### Imagens de Arquivo
- **SEMPRE** color grade amber/sepia (nunca raw/crua)
- **SEMPRE** film grain leve (textura, nao distorcao)
- **SEMPRE** Ken Burns lento (zoom ou pan; nunca estatico)
- **SEMPRE** dissolve entre imagens (nunca hard cut, exceto impacto)
- 40-60 imagens por video de 15 min (sem repeticao visual)

### Thumbnails
- Fundo escuro (#0D0D0D)
- Texto bold amarelo quente (#F5C518), max 3-5 palavras
- Imagem central: produto vintage, rosto de epoca, ou cena nostalgica
- Badge de decada opcional (canto: "80s", "90s") em vermelho escuro
- **SEM** Matt on-camera
- **SEM** setas vermelhas, circulos, rostos chocados (zero clickbait visual)
- Template CONSISTENTE para reconhecimento instantaneo

### Tipografia
- Retro/typewriter: Courier Prime, American Typewriter, ou Playfair Display
- Efeito typewriter ou fade suave (nunca neon/glow)

---

## Intro / Outro

### Intro Padrao (5s)
1. Som de fita VHS sendo inserida + TV ligando
2. Static rapido (1s)
3. Logo aparece com efeito VHS rewind
4. Riff curto de acoustic guitar (quente, nao alto)
5. Total: 5 segundos exatos

### Intro "Pull Up a Chair" (confissoes)
1. Tela preta, 2s silencio
2. Som de grilos texanos
3. Voz: "Hey. It's Math. Pull up a chair."
4. Imagem emerge lentamente (paisagem/cena noturna)

### Outro (20s)
- Dois videos recomendados
- Musica de fundo suave
- Texto: "More stories. Same chair."
- Logo centro-inferior

---

## Formato de Video

- **Resolucao:** 1920x1080 (16:9)
- **Long-form:** 15-25 min (compilacoes), 12-16 min (confissoes), 14-18 min (Sunset Strip)
- **Short-form:** 8-12 min (compilacoes rapidas)
- **Shorts:** 15-60s extraidos dos long-form
- **Transicoes:** VHS glitch/static entre segmentos, dissolve entre imagens
- **Ken Burns:** Zoom lento ou pan em TODAS as imagens estaticas
- **Color grade:** Amber/sepia em TODO frame

---

## Prompt Base — Midjourney v7

### Estilo Visual
```
warm amber nostalgic photograph, 1980s americana, suburban small town,
soft film grain, golden hour light, Kodachrome color palette,
slightly faded vintage photograph, nostalgic warm tones,
35mm film texture, soft depth of field
```

### Parametros Obrigatorios
```
--ar 16:9 --style raw --v 7 --q 2 --stylize 500 --chaos 15
```

### Negative Prompt
```
--no text, watermark, modern, digital, clean, bright, neon, anime, cartoon, cheerful, corporate, stock photo, AI-generated look, oversaturated
```

### Variacoes por Pilar

**Rewound (compilacoes):**
```
product photography style, catalog aesthetic, commercial lighting,
slightly worn vintage item, period-accurate details
```

**Pull Up a Chair (confissoes):**
```
cinematic still, atmospheric, moody lighting, American landscape,
empty spaces, golden hour, melancholic beauty, solitude
```

**Sunset Strip (bandas):**
```
1980s Sunset Strip Hollywood, neon lights at night, rock concert photography,
backstage atmosphere, smoky club interior, Whisky a Go Go aesthetic
```

---

## Pipeline de Agentes (mesmo pipeline universal)

| Fase | Agente | Nota para este canal |
|------|--------|---------------------|
| 1 | Argos | Pesquisar nostalgia topics, trends, gaps competitivos |
| 1 | Hermes | SEO em ingles, keywords nostalgia |
| 2 | Morrigan | Roteiro em INGLES, tom do Matt (ver persona_matt.md) |
| 2 | Nyx | Storyboard com 100% imagens estaticas |
| 3 | Orfeu | **Modo ElevenLabs** — texto limpo sem tags Suno |
| 3 | Goetia | Prompts MJ com estilo amber/nostalgic (nao biblical/dark) |
| 3.5 | Phantasma | ffmpeg/prometheus — Ken Burns + dissolve + amber grade |
| 4 | Medusa | Thumbnail dark + amarelo + vintage image |
| 4 | Sibila | Metadata em ingles, tags nostalgia |
| 4 | Caronte | Upload private |
| 5 | Anubis | Metricas |
| 5 | Midas | Financeiro |

---

## Regras Absolutas

1. **NUNCA** mostrar rosto do Matt (canal e voz-only)
2. **NUNCA** politica no canal (ver persona_matt.md)
3. **NUNCA** imagem sem color grade amber/sepia
4. **NUNCA** hard cut entre imagens (sempre dissolve ou VHS glitch)
5. **NUNCA** musica alta demais (voz e o centro)
6. **NUNCA** nomear esposa, filhos ou irmao do Matt
7. **SEMPRE** 40-60 imagens por 15 min de video (sem repeticao)
8. **SEMPRE** Ken Burns em todas as imagens
9. **SEMPRE** fechar confissoes com momento de humor sutil
10. **SEMPRE** tom conversacional (nunca performatico)
