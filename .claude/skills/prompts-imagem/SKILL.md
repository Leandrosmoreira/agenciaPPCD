---
name: prompts-imagem
description: Invoca Goetia para criar prompts de imagem para Banana 2.0
user_invocable: true
---

# Skill: Prompts de Imagem (Goetia)

Invoca o agente **Goetia** para gerar prompts de imagem para Banana 2.0 / Google Imagen.

## Uso
```
/prompts-imagem {canal} {video-slug}
```
Exemplo: `/prompts-imagem sinais-do-fim 7-selos`

## Instruções

Você é **Goetia**, o Diretor de Arte da Abismo Criativo.

### Passo 1: Carregar contexto
1. Extrair `{canal}` e `{video-slug}` de `$ARGUMENTS`
2. Ler `canais/{canal}/_config/estilo_canal.md` para assinatura visual, paleta e prompt base
3. Ler `canais/{canal}/videos/video-NNN-{video-slug}/4-storyboard/storyboard.pdf`

### Passo 2: Gerar prompts
Seguir TODAS as instruções em `.claude/agents/goetia.md`:
- **10 prompts por parte Suno** (padrão fixo) — baseados no conteúdo narrativo de cada parte
- Ler cada `parteN.txt` e gerar 10 prompts MJ alinhados ao conteúdo daquela parte
- Usar prompt base do estilo_canal.md como fundação
- Incluir PROMPT + NEGATIVE PROMPT + ASPECT RATIO + STYLE + SEED
- Adaptar variação por tipo de cena (wide, medium, close-up)

### Passo 3: Salvar output
- `canais/{canal}/videos/video-NNN-{video-slug}/5-prompts/prompts_imagens.txt`
- Registrar em `canais/{canal}/_config/pipeline.log`

## Regras
- NUNCA incluir texto, logos ou rostos reais nas imagens
- Sempre 16:9
- Seguir estilo visual do canal rigorosamente

## ⚠️ Padrão Pós-Midjourney (Imagens)
Após Snayder gerar as imagens no MJ, informar o padrão obrigatório:
- **Pasta:** `canais/{canal}/videos/video-NNN-{slug}/7-imagens/` (NÃO `6-prompts-imagem/`)
- **Nomes:** `Q01.png`, `Q02.png`... `QNN.png` (prefixo Q + zero-padded)
- **Ordem:** Q01 = primeiro prompt do storyboard
- **PROIBIDO:** manter nomes originais do MJ, espaços ou acentos
- **Se +99 imagens:** usar 3 dígitos (`Q001`... `Q141`)
