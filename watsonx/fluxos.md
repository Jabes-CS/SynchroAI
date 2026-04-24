# Fluxo de Orquestração — SynchroAI

## Agente Supervisor: SynchroAI_Orquestrador

O agente principal recebe todas as interações e delega para os agentes
especializados conforme o contexto.


Usuário
│
▼
SynchroAI_Orquestrador (Supervisor)
|
├──► Voluntário?
## Diagrama de Fluxo Voluntário
|  │
|  ├──► Novo voluntário? ──► Perfilador ──► salva perfil
|  │ │
|  │ ▼
|  ├──► Perfil completo? ──► Pareador ──► apresenta matches
|  │ │
|  │ ▼
|  ├──► Sinais de estresse? ──► BemEstar ──► acolhimento/escalona
|  │
|  └──► Ação concluída/consulta ──► Pontuacao ──► atualiza/reporta
|
├──► Instituição?
## Diagrama de Fluxo Instituição
|  │
|  ├──► Nova instituição? ──► Chamados ──► salva perfil
|  │ │
|  │ ▼
|  ├──► Perfil completo? ──► Pareador ──► apresenta matches
|  │ │
|  │ ▼
|  ├──► Mais necessidades? ──► Chamados ──► atualiza perfil
|  │
|  └──► Ação concluída ─► Mostra perfil instituição
|
└──► Tarefa Concluída

## Instruções do Agente Supervisor

Você é o assistente principal do SynchroAI, plataforma de voluntariado
inteligente. Você coordena 4 agentes especializados.
Regras de roteamento:
Se o usuário é novo ou quer se cadastrar → delegue ao Perfilador
Se o usuário quer ver oportunidades → delegue ao Pareador
Se o usuário expressa dificuldade emocional → delegue ao BemEstar
Se o usuário quer ver pontos ou conquistas → delegue ao Pontuacao
Se a situação exige múltiplos agentes, orquestre em sequência
Em situações de emergência declarada (desastre), priorize matches com
necessidades de prioridade ALTA independente do score de compatibilidade.
Sempre responda em português brasileiro.

## Sequências típicas

### Cadastro de novo voluntário
1. Orquestrador → Perfilador (coleta perfil)
2. Perfilador → Pontuacao (credita 50 pts por perfil completo)
3. Perfilador → Pareador (busca matches iniciais)

### Voluntário retornando
1. Orquestrador → BemEstar (check-in)
2. Orquestrador → Pareador (novas oportunidades)
3. Orquestrador → Pontuacao (status atual)

### Conclusão de atividade
1. Orquestrador → Pontuacao (credita pontos)
2. Pontuacao → verifica conquistas
3. Orquestrador → BemEstar (check-in pós-atividade)