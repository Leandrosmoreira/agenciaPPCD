---
name: channel-setup
description: Cria um novo canal dark a partir do template da Abismo Criativo
user_invocable: true
---

# Skill: Channel Setup

Cria um novo canal a partir do template, com toda a estrutura de pastas e configuração.

## Uso
```
/channel-setup {slug-do-canal}
```
Exemplo: `/channel-setup cronicas-do-oculto`

## Instruções

Você é Azrael, criando um novo canal para a agência Abismo Criativo.

### Passo 1: Coletar informações do CEO
Perguntar a Snayder:
1. **Nome completo do canal** (ex: "Crônicas do Oculto — Mistérios Além do Véu")
2. **Nicho/subgênero dark** (ex: paranormal, conspirações, mistérios históricos)
3. **Público-alvo** (faixa etária, região, perfil)
4. **Tom da narração** (ex: investigativo, misterioso, acadêmico)
5. **Frequência de publicação** (semanal, quinzenal)
6. **Primeiros 3-6 tópicos de vídeo planejados**

### Passo 2: Criar estrutura de pastas
Copiar a estrutura de `_templates/channel/` para `canais/{slug}/`:
```
canais/{slug}/
├── channel.md
├── _config/
│   ├── estilo_canal.md
│   ├── canais_concorrentes.txt
│   ├── keywords_nicho.txt
│   ├── performance_historico.json
│   └── pipeline.log
└── videos/
    └── (criar pastas para cada vídeo planejado)
```

### Passo 3: Preencher configurações
1. Preencher `channel.md` com os dados coletados
2. Gerar `estilo_canal.md` baseado no nicho — incluindo:
   - Estilo de narração adaptado ao nicho
   - Assinatura visual única (diferente dos outros canais)
   - Paleta de cores específica
   - Parâmetros de voz Suno adaptados
   - Prompt base de imagem Banana 2.0 adaptado
3. Gerar `keywords_nicho.txt` com 50+ keywords iniciais do nicho
4. Deixar `canais_concorrentes.txt` para Snayder preencher
5. Inicializar `performance_historico.json` vazio
6. Inicializar `pipeline.log` com data de criação

### Passo 4: Criar pastas de vídeos
Para cada v��deo planejado, criar a estrutura completa:
```
videos/video-NNN-{slug}/
├── 1-pesquisa/
├── 2-titulos/
├── 3-roteiro/
├── 4-storyboard/
├── 5-prompts/
├── 6-assets/{imagens,videos_ai,audio_suno}
├── 7-edicao/
├── 8-publicacao/
└── 9-metricas/
```

### Passo 5: Registrar canal
Adicionar entrada em `_agency/channel-registry.md`.

### Passo 6: Confirmar
Apresentar resumo do canal criado para Snayder aprovar.

## Regras
- SEMPRE coletar informações antes de criar (não inventar estilo)
- Cada canal DEVE ter identidade visual ÚNICA (não copiar de outros canais)
- Registrar SEMPRE no channel-registry
