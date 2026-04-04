---
name: queue-status
description: Dashboard da fila de producao — ver status de todos os agentes e tarefas
user_invocable: true
---

# Skill: Queue Status

Mostra o status completo da fila de produção assíncrona.

## Uso
```
/queue-status                    → Visão geral completa
/queue-status {canal}            → Filtrar por canal
/queue-status --active           → Só tarefas ativas e checkpoints
```

## Instruções

### Passo 1: Ler a fila
1. Ler `_agency/queue/queue.json`
2. Se argumento fornecido, filtrar por canal
3. Agrupar tarefas por status

### Passo 2: Apresentar dashboard

Formato de saída:

```
═══ ABISMO CRIATIVO — Fila de Produção ═══

ATIVOS ({N} tarefas em progresso)
  🟢 {Agente} → {canal}/{video} (Fase {N}: {step})
  🟢 {Agente} → {canal}/{video} (Fase {N}: {step})

CHECKPOINTS ({N} aguardando aprovação)
  🟠 {canal}/{video} → Fase {N} (desde {data})
  🟠 {canal}/{video} → Fase {N} (desde {data})

EDIÇÃO MANUAL ({N} no CapCut)
  🔵 {canal}/{video} → Aguardando Snayder

FILA ({N} tarefas prontas para executar)
  ⚪ {canal}/{video} → Fase {N} (prioridade: {label})

BLOQUEADOS ({N} aguardando dependências)
  ⬛ {canal}/{video} → Fase {N} (depende de: {dependency})

CONCLUÍDOS HOJE ({N})
  ✅ {canal}/{video} → Fase {N} ({hora})

─── Agentes ───
  Ociosos: {lista de agentes sem tarefa}
  Trabalhando: {lista de agentes com tarefa ativa}

─── Throughput ───
  Tarefas concluídas hoje: {N}
  Vídeos em produção: {N}
  Canais ativos: {N}

Próximo: /dispatch para executar | /approve para aprovar checkpoints
```

### Passo 3: Atualizar dashboard-state.json
Após gerar o status, salvar estado resumido em `_agency/queue/dashboard-state.json` para o office.html consumir:

```json
{
  "lastUpdated": "{timestamp}",
  "tasks": [{tarefa resumida}],
  "agentStatus": {
    "argos": "idle|working|waiting",
    "hermes": "idle|working|waiting"
  },
  "stats": {
    "active": N,
    "checkpoints": N,
    "queued": N,
    "blocked": N,
    "completedToday": N
  }
}
```

## Regras
- Leitura apenas — NUNCA modificar a fila neste skill
- Sempre mostrar contadores e resumo
- Identificar gargalos (agentes sobrecarregados vs ociosos)
