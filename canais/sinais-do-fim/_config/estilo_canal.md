# ESTILO DO CANAL — SINAIS DO FIM — Passagens do Apocalipse

## Identidade
- **Nome:** Sinais do Fim — Passagens do Apocalipse
- **Nicho:** Dark biblical storytelling / Escatologia
- **Idioma:** Português Brasileiro
- **Público:** Evangélicos e interessados em escatologia, 25-55 anos, Brasil
- **Tom:** Médio — conecta profecias com eventos reais sem extremismo

## Estilo de Narração
- Narrador sério e misterioso (documentário)
- Voz: homem de 55-65 anos, grave, locutor de rádio experiente
- Ritmo lento e deliberado com pausas dramáticas
- Nunca grita, nunca é cômico, nunca é leve
- Frases curtas e impactantes

## Assinatura Visual
- **Foreground:** Ilustrações bíblicas medievais em CORES RICAS (anjos, bestas, profetas)
- **Background:** Mundo moderno em PRETO E BRANCO (cidades destruídas, explosões, tecnologia)
- **Contraste:** Sujeito bíblico sempre vibrante vs. mundo sempre monocromático
- **Elementos fixos:** Fogo, fumaça, nuvens dramáticas, cinzas flutuantes

## Paleta de Cores
- Preto (#0A0A0A) — fundo e sombras
- Vermelho sangue (#8B0000) — fogo, ira, urgência
- Dourado envelhecido (#C5A355) — divino, sagrado
- Branco sujo (#E8E0D0) — luz divina

## Thumbnails
- 1280×720px, 16:9
- 70% imagem + 30% texto (max 5 palavras)
- Fonte bold gótica com outline preto
- Cor: Branco com outline vermelho (#8B0000) OU dourado (#C5A355)
- Logo "SINAIS DO FIM" semi-transparente no canto inferior esquerdo

## Áudio — Motor de Narração
- **Motor:** suno
- **Voice ID (ElevenLabs):** (nao usado — Suno)

## Áudio (Suno) — PADRÃO APROVADO v2 (2026-04-12)
- Formato obrigatório de cada parte Suno:
```
[Voice: Deep male narrator, 45-55 years old, energetic gravelly radio host voice, fast-paced confident delivery with sharp emphasis on key words, punchy rhythm with short dramatic beats, Brazilian Portuguese accent, voice rises and falls with urgency, authoritative and direct, NOT singing, NOT whispering, investigative journalism tone not slow sermon]
[Background: Dark cinematic suspense soundtrack with pulse, deep electronic drones, low cello stabs, percussive tension hits on key revelations, ominous reverb-heavy atmosphere, music responds to narration — swells on reveals, drops on short pauses, slightly present but never competing with voice]
[Style: Fast-paced documentary thriller narration, investigative journalism urgency, prophetic tone, sharp dramatic beats, forward momentum]
```
- Pausas com duração: `[pausa 1s]` / `[pausa 0.5s]`
- Silêncios dramáticos: `[Silêncio de 1 segundo. Drone grave, seco.]`
- Cues musicais inline: `[trilha pulsa grave]` / `[trilha dark entra com força]` / `[voz mais firme]`
- Ritmo: **fast-paced** (NÃO middle-paced)
- Limite: **2.000–2.500 chars por parte** — OBRIGATÓRIO contar caracteres antes de salvar. Se exceder 2.500, criar parte adicional (ex: 4.1, 4.2 ou parte 6). Nunca estourar o limite.
- **Números e anos SEMPRE por extenso:** "2025" → "dois mil e vinte e cinco" | "1.700" → "mil e setecentos" | "350 milhões" → "trezentos e cinquenta milhões". SEM EXCEÇÃO.

## Formato de Vídeo
- 16:9, 1080p mínimo
- Duração: **13-14 minutos** (padrão revisado após video-002) ou 8-12 minutos (rápido)
- Edição: CapCut (manual)
- Efeito: Ken Burns (zoom lento) em imagens estáticas — TODAS as cenas usam este efeito
- **NYX (Storyboard):** Marcar 100% dos quadros como "Imagem estática" — NUNCA marcar quadros como "Vídeo/Clipe" neste canal

## Diretrizes de Roteiro (Morrigan) — Lições Aprendidas
- video-002: duração ficou longa (15:30) + repetição temática entre atos
- A partir de video-003: máximo 13-14 min de narração
- Cada ato deve cobrir UM ângulo único — sem retornar a ponto já coberto
- Revisão obrigatória antes de entregar: checar se algum dado/argumento aparece 2x

## Stack Visual (Midjourney v7)
- **Ferramenta:** Midjourney v7 — APENAS IMAGENS (Goetia)
- **Agente de vídeo:** **Phantasma ATIVO** — editor MoviePy (Ken Burns + color grading + transições)
- **100% do storyboard = imagens estáticas (Midjourney)** → Phantasma anima via MoviePy
- **Parâmetros fixos:** `--ar 16:9 --style raw --v 7 --q 2 --stylize 750`
- **Chaos:** `--chaos 20` (variedade controlada)
- **Negative:** `--no text, watermark, logo, anime, cartoon, cheerful, modern colors in foreground, blurry`
- **Seed base:** 847200 (incrementar +1 por quadro para reprodutibilidade)
- **Estilo global:** `--sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750` ✓ APROVADO 2026-04-06

## Pipeline de Agentes — Sinais do Fim
| Fase | Agente | Status |
|------|--------|--------|
| Pesquisa | Argos | ✓ ATIVO |
| SEO | Hermes | ✓ ATIVO |
| Roteiro | Morrigan | ✓ ATIVO |
| Storyboard | Nyx | ✓ ATIVO — gerar APENAS imagens (sem marcar quadros como vídeo) |
| Prompts Imagem | Goetia | ✓ ATIVO — 100% do storyboard |
| Montagem | Phantasma | ✓ ATIVO — editor MoviePy (Ken Burns + color grading + transições) |
| Narração | Orfeu | ✓ ATIVO |
| Thumbnail | Medusa | ✓ ATIVO |
| Metadata | Sibila | ✓ ATIVO |
| Upload | Caronte | ✓ ATIVO |
| Métricas | Anubis | ✓ ATIVO |

## Prompt Base de Imagem (Midjourney v7) — Design Aprovado
Resultado visual aprovado por Snayder em 2026-04-06. Este é o DNA visual definitivo do canal.

**Descrição do design aprovado:**
Figura clássica/medieval em CORES RICAS e vibrantes (carmesim, dourado, ocre) em plano frontal.
Cidade/mundo em PRETO E BRANCO completamente desaturado ao fundo.
Brasas e partículas de fogo flutuando por toda a cena.
Iluminação chiaroscuro dramática vinda do alto.
Textura de filme 35mm + lens flares anamórficos.

**Prompt base aprovado (colar no MJ sem parâmetros para Style Creator):**
```
colorful vivid prophet in crimson and ochre robes in foreground, black and white desaturated modern city in background, chiaroscuro dramatic lighting, fire glow floating ash particles, strong contrast vibrant medieval subject versus monochrome modern world, ornate decorative borders, aged parchment texture, 35mm film grain, anamorphic lens flares, epic surreal prophetic atmosphere
```

**Comando /imagine completo (para geração direta):**
```
/imagine prompt: [DESCRIÇÃO DA CENA] colorful vivid [SUJEITO] in [CORES] in foreground, black and white desaturated [CENARIO MODERNO] in background, chiaroscuro dramatic lighting, fire glow and floating ash embers, strong contrast vibrant foreground versus monochrome background, 35mm film grain, anamorphic lens flares, epic surreal prophetic apocalyptic atmosphere --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed [SEED] --no text, watermark, anime, cartoon, cheerful, modern colors in foreground, blurry
```

## Sujeitos Bíblicos Recorrentes
- Anjos medievais (asas detalhadas, auréola, vestes ornamentadas)
- Cordeiro com 7 chifres e 7 olhos
- Cavaleiros do Apocalipse (branco, vermelho, preto, pálido)
- Bestas de múltiplas cabeças
- Profetas em mantos (João, Daniel, Enoque)
- Trono divino com luz radiante
- Pergaminhos e selos de cera

## Cenários Modernos P&B Recorrentes
- Cidades destruídas (ruínas, escombros, prédios desabando)
- Explosão nuclear (cogumelo atômico)
- Multidões em pânico
- Tecnologia e vigilância (câmeras, telas, microchips)
- Conflitos militares (tanques, explosões, refugiados)
- Desastres naturais (terremotos, tsunamis, vulcões)
- Espaço/cosmos (lua de sangue, estrelas caindo, sol negro)

## Referências Temáticas Obrigatórias
- Apocalipse, Daniel, Ezequiel, Joel, Mateus 24
- Tópicos evergreen: Marca da Besta, Nephilim, Arrebatamento, 7 Selos, 7 Trombetas
- Conexão profecia × evento real verificável
