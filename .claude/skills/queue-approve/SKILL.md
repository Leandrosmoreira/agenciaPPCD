---
name: approve
description: Aprovar checkpoints em batch — liberar tarefas bloqueadas para continuar
user_invocable: true
---

# Skill: Approve

Aprova checkpoints pendentes, desbloqueando as próximas fases do pipeline.

## Uso
```
/approve                                → Listar todos os checkpoints pendentes
/approve {task-id}                      → Aprovar tarefa específica
/approve {task-id1} {task-id2} ...      → Aprovar múltiplas tarefas
/approve --all                          → Aprovar TODOS os checkpoints
/approve --all-fase1                    → Aprovar todos os checkpoints da Fase 1
/approve --channel {canal}              → Aprovar todos os checkpoints de um canal
```

## Instruções

### Modo Listagem (sem argumentos)

1. Ler `_agency/queue/queue.json`
2. Filtrar tarefas com `status == "checkpoint"` ou `status == "manual_edit"`
3. Apresentar tabela:

```
═══ CHECKPOINTS PENDENTES ═══

#  | ID                        | Canal           | Vídeo           | Fase | Desde
1  | sdf-001-fase1-pesquisa    | sinais-do-fim   | 7-selos         | 1    | 04/04 23:05
2  | sdf-002-fase1-pesquisa    | sinais-do-fim   | marca-da-besta  | 1    | 04/04 23:08
3  | cdo-001-fase2-criacao     | cronicas-oculto | ouija           | 2    | 04/04 23:15

EDIÇÃO MANUAL:
4  | sdf-001-manual-edicao     | sinais-do-fim   | 7-selos         | -    | 04/04 23:20
   → video_final.mp4 pronto? Confirme para avançar para publicação.

Aprovar quais? (números, IDs, --all, --all-fase{N}, ou --channel {canal})
```

### Modo Aprovação

1. Identificar quais tarefas aprovar (por ID, número, ou filtro)
2. Para cada tarefa aprovada:
   a. Se `status == "checkpoint"`:
      - Mudar para `"approved"`
      - Registrar `completedAt`
   b. Se `status == "manual_edit"`:
      - Verificar que `canais/{canal}/videos/{video}/7-edicao/video_final.mp4` existe
      - Se não existe: avisar Snayder e não aprovar
      - Se existe: mudar para `"approved"`
3. **DESBLOQUEAR dependentes:**
   - Varrer TODAS as tarefas com `status == "blocked"`
   - Se TODAS as dependências da tarefa têm status `"approved"` ou `"completed"`
   - Mudar status para `"queued"`
4. Atualizar `lastUpdated` em queue.json
5. Registrar no pipeline.log do canal

### Output

```
APROVAÇÃO CONCLUÍDA

Aprovados: {N} tarefas
  ✅ {id1} — {canal}/{video} Fase {N}
  ✅ {id2} — {canal}/{video} Fase {N}

Desbloqueados: {N} tarefas agora na fila
  🔓 {id3} — {canal}/{video} Fase {N} (agentes: {lista})
  🔓 {id4} — {canal}/{video} Fase {N} (agentes: {lista})

Execute /dispatch para iniciar as tarefas desbloqueadas.
```

## Regras
- NUNCA aprovar automaticamente — sempre requer ação explícita de Snayder
- Mostrar RESUMO do que foi produzido antes de pedir aprovação
- Para manual_edit: VERIFICAR que video_final.mp4 existe
- Após aprovar: SEMPRE escanear e desbloquear tarefas dependentes
- Registrar TUDO no pipeline.log
