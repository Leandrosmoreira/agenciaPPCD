# Registro de Agentes — Abismo Criativo

| Persona | Função | Tipo | Arquivo | Fase |
|---------|--------|------|---------|------|
| **Azrael** | Orquestrador Mestre | agência | `azrael.md` | Todas |
| **Argos** | Pesquisador de Nicho | compartilhado | `argos.md` | 1 |
| **Hermes** | Analista SEO + Títulos | compartilhado | `hermes.md` | 1 |
| **Morrigan** | Criadora de Roteiro | canal-específico | `morrigan.md` | 2 |
| **Nyx** | Criadora de Storyboard | canal-específico | `nyx.md` | 2 |
| **Goetia** | Prompts de Imagem (Banana 2.0) | canal-específico | `goetia.md` | 3 |
| **Phantasma** | Prompts de Vídeo (Veo 3) | canal-específico | `phantasma.md` | 3 |
| **Orfeu** | Locutor + Trilha (Suno) | canal-específico | `orfeu.md` | 3 |
| **Medusa** | Criadora de Thumbnails | canal-específico | `medusa.md` | 4 |
| **Sibila** | Metadata YouTube | compartilhado | `sibila.md` | 4 |
| **Caronte** | Agente de Upload | compartilhado | `caronte.md` | 4 |
| **Anubis** | Analista de Métricas | compartilhado | `anubis.md` | 5 |

## Tipos de Agente
- **agência**: Opera no nível da agência, acima dos canais
- **compartilhado**: Funciona para qualquer canal, lê config do canal em runtime
- **canal-específico**: Adapta output baseado no `estilo_canal.md` do canal ativo

## Como Adicionar Novo Agente
1. Criar arquivo `.md` em `.claude/agents/` com nome da persona
2. Adicionar entrada nesta tabela
3. Definir em qual fase do pipeline o agente atua
4. Atualizar `CLAUDE.md` se o agente entra no pipeline principal
