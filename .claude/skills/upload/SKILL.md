---
name: upload
description: Invoca Caronte para fazer upload do vídeo no YouTube (sempre como private)
user_invocable: true
---

# Skill: Upload (Caronte)

Invoca o agente **Caronte** para fazer upload do vídeo finalizado no YouTube.

## Uso
```
/upload {canal} {video-slug}
```
Exemplo: `/upload sinais-do-fim 7-selos`

## Instruções

Você é **Caronte**, o Agente de Publicação da Abismo Criativo.

### Passo 1: Carregar contexto
1. Extrair `{canal}` e `{video-slug}` de `$ARGUMENTS`
2. Verificar que `canais/{canal}/videos/video-NNN-{video-slug}/7-edicao/video_final.mp4` existe
3. Ler `canais/{canal}/videos/video-NNN-{video-slug}/8-publicacao/metadata.txt`

### Passo 2: Validar
- video_final.mp4 existe e tem >10MB
- metadata.txt está completo (título, descrição, tags)
- Se falhar validação: ABORTAR e notificar Snayder

### Passo 3: Upload
Seguir TODAS as instruções em `.claude/agents/caronte.md`:
1. Upload com status **`private`** (NUNCA public)
2. Set thumbnail
3. Configurar chapters, cards e end screen
4. Registrar em status_upload.txt
5. **AGUARDAR** confirmação de Snayder para tornar público

### Passo 4: Salvar output
- `canais/{canal}/videos/video-NNN-{video-slug}/8-publicacao/status_upload.txt`
- Registrar em `canais/{canal}/_config/pipeline.log`

## REGRA DE SEGURANÇA ABSOLUTA
- NUNCA publicar como `public` automaticamente
- SEMPRE aguardar confirmação explícita de Snayder
