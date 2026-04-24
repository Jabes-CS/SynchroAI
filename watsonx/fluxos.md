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