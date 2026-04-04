---
name: queue-add
description: Adicionar videos a fila de producao assincrona da Abismo Criativo
user_invocable: true
---

# Skill: Queue Add

Adiciona um ou mais vídeos à fila de produção assíncrona.

## Uso
```
/queue-add {canal} {video-slugs...} [--priority urgent|high|normal|low|backlog]
```
Exemplos:
```
/queue-add sinais-do-fim video-001-7-selos video-002-marca-da-besta --priority high
/queue-add cronicas-do-oculto video-001-ouija --priority urgent
```

## Instruções

### Passo 1: Validar argumentos
1. Extrair `{canal}` e lista de `{video-slugs}` de `$ARGUMENTS`
2. Verificar que `canais/{canal}/` existe
3. Para cada video-slug, verificar que `canais/{canal}/videos/{video-slug}/` existe
4. Se não existir, criar a estrutura de pastas do vídeo
5. Extrair prioridade (default: `normal`)

### Passo 2: Gerar tarefas para cada vídeo
Para cada vídeo, criar 6 tarefas encadeadas com dependências:

```
{prefix}-fase1-pesquisa    → status: "queued"   (sem dependência)
{prefix}-fase2-criacao     → status: "blocked"  (depende de fase1)
{prefix}-fase3-assets      → status: "blocked"  (depende de fase2)
{prefix}-manual-edicao     → status: "blocked"  (depende de fase3)
{prefix}-fase4-publicacao  → status: "blocked"  (depende de manual-edicao)
{prefix}-fase5-analise     → status: "blocked"  (depende de fase4)
```

O `{prefix}` é gerado como: `{canal-abreviado}-{numero-video}`
Exemplo: `sdf-001`, `cdo-001`

### Passo 3: Estrutura de cada tarefa
```json
{
  "id": "{prefix}-fase{N}-{step}",
  "channel": "{canal}",
  "videoSlug": "{video-slug}",
  "phase": {N},
  "step": "{step}",
  "agents": ["agent1", "agent2"],
  "status": "queued|blocked",
  "priority": 3,
  "priorityLabel": "normal",
  "dependencies": ["{id-da-tarefa-anterior}"],
  "checkpointAfter": true|false,
  "createdAt": "{timestamp}",
  "startedAt": null,
  "completedAt": null,
  "assignedTo": null,
  "output": null
}
```

### Mapeamento fase → agentes:
| Fase | Step | Agentes | Checkpoint? |
|------|------|---------|-------------|
| 1 | pesquisa | argos, hermes | sim |
| 2 | criacao | morrigan, nyx | sim |
| 3 | assets | goetia, phantasma, orfeu | sim |
| - | manual-edicao | (snayder) | sim |
| 4 | publicacao | medusa, sibila, caronte | sim |
| 5 | analise | anubis | não |

### Prioridades:
| Valor | Label | Uso |
|-------|-------|-----|
| 1 | urgent | Tópico trending, janela temporal curta |
| 2 | high | Canal principal, conteúdo prioritário |
| 3 | normal | Produção regular |
| 4 | low | Evergreen, sem pressa |
| 5 | backlog | Ideias para depois |

### Passo 4: Salvar no queue.json
1. Ler `_agency/queue/queue.json`
2. Adicionar as novas tarefas ao array `tasks`
3. Atualizar `lastUpdated`
4. Salvar o arquivo

### Passo 5: Confirmar
Mostrar resumo para Snayder:
```
FILA ATUALIZADA — {N} tarefas adicionadas

Canal: {canal}
Vídeos: {lista}
Prioridade: {label}
Total na fila: {total}

Próximo passo: execute /dispatch para iniciar produção
```

## Regras
- NUNCA duplicar tarefas que já existem no queue.json
- Verificar por videoSlug + phase antes de adicionar
- Múltiplos vídeos do MESMO canal podem ser adicionados de uma vez
- Tarefas de vídeos DIFERENTES não têm dependência entre si
