# 🤖 SynchroAI — Watsonx Orchestrate Agents

Esta pasta contém a configuração dos agentes de IA do SynchroAI,
construídos com o **IBM watsonx Orchestrate Agent Development Kit (ADK)**.

## Estrutura

- `agents/` — Definições dos agentes em YAML (formato oficial IBM)
- `tools/` — Funções Python decoradas com `@tool` que os agentes usam
- `fluxo.md` — Documentação de como os agentes conversam entre si
- `.env` — Credenciais do watsonx Orchestrate (não commitar!)

## Agentes

| Agente | Arquivo | Função |
|--------|---------|--------|
| Perfilador | `agents/perfilador.yaml` | Coleta habilidades do voluntário |
| Pareador | `agents/pareador.yaml` | Casa voluntários com necessidades |
| Bem-estar | `agents/bem-estar.yaml` | Previne burnout via revezamento |
| Pontuação | `agents/pontuacao.yaml` | Gamificação e retenção |

## Como rodar

```bash
# Na raiz do projeto, com o venv ativado
orchestrate env activate synchroai
orchestrate agents import -f watsonx/agents/perfilador.yaml
orchestrate chat start
```

## Documentação oficial

- [Getting Started](https://developer.watson-orchestrate.ibm.com/getting_started/installing)
- [Agent Specs](https://developer.watson-orchestrate.ibm.com/agents/)