---
name: dispatch
description: Dispatcher — executa a proxima tarefa disponivel na fila de producao
user_invocable: true
---

# Skill: Dispatch

O coração do sistema assíncrono. Pega a próxima tarefa disponível na fila e executa o agente correspondente. Ao terminar, automaticamente pega a próxima.

## Uso
```
/dispatch                     → Executar próxima tarefa da fila
/dispatch --loop              → Continuar executando até fila vazia ou checkpoint
/dispatch --channel {canal}   → Só executar tarefas de um canal específico
```

## Instruções

Você é **Azrael**, o Dispatcher da Abismo Criativo.

### Algoritmo de Seleção

```
1. Ler _agency/queue/queue.json
2. Filtrar tarefas com status == "queued"
3. Para cada, verificar:
   a. Todas as dependências têm status "approved" ou "completed"
   b. Não existe lock em _agency/queue/locks/{task-id}.lock
4. Ordenar por:
   a. Prioridade (1=urgent primeiro)
   b. Número da fase (menores primeiro — avançar vídeos)
   c. Data de criação (FIFO)
5. Selecionar a primeira tarefa elegível
```

### Execução da Tarefa

```
1. Criar lock: _agency/queue/locks/{task-id}.lock
   {
     "taskId": "{id}",
     "agent": "{agente principal}",
     "lockedAt": "{timestamp}",
     "expiresAt": "{timestamp + 30min}"
   }

2. Atualizar queue.json:
   - status → "in_progress"
   - startedAt → timestamp atual
   - assignedTo → nome do agente

3. Invocar agente(s) conforme a fase:

   FASE 1 (pesquisa):
     → Invocar Argos (.claude/agents/argos.md)
     → Invocar Hermes (.claude/agents/hermes.md)

   FASE 2 (criacao):
     → Invocar Morrigan (.claude/agents/morrigan.md)
     → Invocar Nyx (.claude/agents/nyx.md)

   FASE 3 (assets): [PARALELO]
     → Invocar Goetia + Phantasma + Orfeu em paralelo

   FASE 4 (publicacao):
     → Invocar Medusa (.claude/agents/medusa.md)
     → Invocar Sibila (.claude/agents/sibila.md)
     → Checkpoint para aprovar metadata
     → Invocar Caronte (.claude/agents/caronte.md)

   FASE 5 (analise):
     → Invocar Anubis (.claude/agents/anubis.md)

   MANUAL-EDICAO:
     → Setar status "manual_edit"
     → Informar Snayder: "Video pronto para CapCut"
     → NÃO avançar — Snayder confirma quando terminar

4. Ao concluir:
   a. Se checkpointAfter == true:
      - status → "checkpoint"
      - Informar Snayder que há checkpoint pendente
   b. Se checkpointAfter == false:
      - status → "completed"
      - Mover para _agency/queue/history/{task-id}.done.json
   c. Remover lock
   d. Registrar em canais/{canal}/_config/pipeline.log
   e. output → lista de arquivos gerados

5. DESBLOQUEAR tarefas dependentes:
   - Varrer todas as tarefas com status "blocked"
   - Se TODAS as dependências estão "approved" ou "completed"
   - Mudar status para "queued"

6. Se --loop: voltar ao passo 1 (próxima tarefa)
   Se não: informar Snayder o que foi feito e o que vem a seguir
```

### Tratamento de Erros
- Se agente falhar: status → "failed", manter lock por 5min, notificar Snayder
- Se lock expirado encontrado: remover e disponibilizar tarefa novamente
- Se fila vazia: informar "Fila vazia. Use /queue-add para adicionar vídeos."

### Output para Snayder
```
DISPATCH — Tarefa executada

Tarefa: {id}
Canal: {canal}
Vídeo: {video}
Fase: {N} ({step})
Agentes: {lista}
Status: {checkpoint|completed}
Arquivos: {lista de outputs}
Duração: {tempo}

Próximas na fila: {N} tarefas
Checkpoints pendentes: {N}
```

## Regras
- NUNCA executar tarefa com lock ativo (não expirado)
- NUNCA pular dependências — respeitar a cadeia
- SEMPRE registrar no pipeline.log do canal
- SEMPRE atualizar dashboard-state.json após cada tarefa
- Se checkpoint: NÃO avançar automaticamente, aguardar /approve
- Fase 3 (assets): executar os 3 agentes em PARALELO (Agent tool)
