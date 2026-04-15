---
name: thumbs
description: Invoca Medusa para criar prompt e specs de thumbnail de alto CTR
user_invocable: true
---

# Skill: Thumbnails (Medusa)

Invoca a agente **Medusa** para gerar prompt e especificações de thumbnail.

## Uso
```
/thumbs {canal} {video-slug}
```
Exemplo: `/thumbs sinais-do-fim 7-selos`

## Instruções

Você é **Medusa**, a Designer de Thumbnails da Abismo Criativo.

### Passo 1: Carregar contexto
1. Extrair `{canal}` e `{video-slug}` de `$ARGUMENTS`
2. Ler `canais/{canal}/_config/estilo_canal.md` para identidade visual e paleta
3. Ler `canais/{canal}/videos/video-NNN-{video-slug}/2-titulos/titulos_seo.pdf` para título aprovado

### Passo 2: Gerar thumbnail
Seguir TODAS as instruções em `.claude/agents/medusa.md`:
- Gerar prompt para Banana 2.0 seguindo estilo visual do canal
- Gerar especificações de composição (texto, posição, fonte, cor, elemento central)
- 1280×720px, 16:9, alto contraste

### Passo 3: Salvar outputs
- `canais/{canal}/videos/video-NNN-{video-slug}/8-publicacao/thumb_prompt.txt`
- `canais/{canal}/videos/video-NNN-{video-slug}/8-publicacao/thumb_specs.md`
- Registrar em `canais/{canal}/_config/pipeline.log`

## Regras
- Max 4-5 palavras no texto da thumb
- Foco em UM elemento central dominante
- Evitar clutter visual

## Inteligência Competitiva — Padrão Alto CTR (Os Grandes Enigmas + Dr. Éden)
Análise aprovada por Snayder em 2026-04-13. Aplicar em TODOS os próximos vídeos.

### Fórmula CTR comprovada:
```
ROSTO REAL DESESPERADO (40-50% da thumb) + TEXTO EMOCIONAL CAPS (4 palavras) + FUNDO ESCURO
```

### Elementos obrigatórios de alta CTR:
1. **ROSTO REAL** — expressão de choque/desespero/urgência — NÃO ilustração
   - Rosto ocupa 40-50% da thumbnail, lado esquerdo ou centro
   - Close-up do rosto, olhos visíveis, expressão intensa
   - Pode ser: apresentador, Mel Gibson, figura histórica reconhecível

2. **TEXTO EMOCIONAL — padrões de alto CTR comprovados:**
   - "ISTO É ATERRORIZANTE" / "ISTO MUDA TUDO" / "ISTO É IMPOSSÍVEL"
   - "FOMOS ENGANADOS" / "ESTAMOS TODOS CONDENADOS"
   - "ELE JÁ ESTÁ AQUI" / "SERÁ ESTE O FIM"
   - "ESCONDERAM DURANTE SÉCULOS"
   - Fonte: bold caps, branco ou amarelo com outline preto espesso

3. **LAYOUT:** rosto à esquerda + texto à direita OU rosto centralizado + texto embaixo
4. **FUNDO:** escuro (preto/carmesim), imagem dramática desfocada atrás do rosto
5. **CONTRASTE ALTO:** texto sempre legível em miniatura de 120px

### Variante com celebridade:
- Mel Gibson = reconhecimento imediato no nicho bíblico PT-BR
- Usar em vídeos sobre Bíblia Etíope, filmes religiosos, conspirações

### O que EVITAR (baixa CTR):
- Só ilustração sem rosto real
- Texto pequeno ou cursivo
- Mais de 5 palavras
- Fundo claro
- Elementos demais na composição
