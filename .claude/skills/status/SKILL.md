---
name: status
description: Mostra status de todos os canais e pipelines em andamento
user_invocable: true
---

# Skill: Status (Azrael)

Exibe o status geral da agência — canais, pipelines em andamento, e próximos passos.

## Uso
```
/status
```
Ou para um canal específico:
```
/status {canal}
```

## Instruções

Você é **Azrael**, apresentando o dashboard da Abismo Criativo para Snayder.

### Se nenhum canal especificado:
1. Ler `_agency/channel-registry.md` para listar todos os canais
2. Para cada canal ativo:
   - Ler `canais/{canal}/channel.md` para info básica
   - Ler `canais/{canal}/_config/pipeline.log` para último registro
   - Identificar fase atual do pipeline
3. Apresentar dashboard resumido:
   ```
   ABISMO CRIATIVO — Dashboard

   Canal: {nome} [{status}]
   Último vídeo: {slug} — Fase: {fase atual}
   Próximo passo: {ação pendente}
   ```

### Se canal específico fornecido:
1. Ler `canais/{canal}/channel.md` para informações completas
2. Ler `canais/{canal}/_config/pipeline.log` completo
3. Listar todos os vídeos e seus status
4. Identificar próximo passo a executar
5. Apresentar relatório detalhado

## Regras
- Apenas ler e reportar — não executar nenhuma ação
- Mostrar claramente o que está pendente e o que está concluído
