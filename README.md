# SynchroAI

### By: Jabes & Nickolas

voluntariado-inteligente/
├── backend/
│   ├── app/
│   │   ├── main.py              # Entry point FastAPI
│   │   ├── database.py          # Conexão PostgreSQL/watsonx.data
│   │   ├── models/              # SQLAlchemy: volunteer, institution, need, match...
│   │   ├── schemas/             # Pydantic (validação de entrada/saída)
│   │   ├── routes/              # Endpoints: /volunteers, /needs, /matches
│   │   └── services/
│   │       └── orchestrate.py   # Integração com watsonx Orchestrate
│   ├── requirements.txt
│   └── .env                     # Credenciais (NUNCA commitar)
├── frontend/
│   ├── src/
│   │   ├── pages/               # Home, Cadastro, Dashboard, Tasks
│   │   ├── components/          # Botões, cards, formulários
│   │   └── App.jsx
│   └── package.json
├── watsonx/
│   ├── agents/                  # Prompts e configs de cada agente
│   │   ├── perfilador.md
│   │   ├── pareador.md
│   │   ├── bem-estar.md
│   │   └── pontuacao.md
│   └── fluxos.md                # Como os agentes conversam entre si
├── docs/
│   ├── README.md
│   ├── ARQUITETURA.md
│   ├── BANCO_DADOS.md
│   └── PITCH.md                 # Roteiro do vídeo
└── .gitignore

### made with ibm watsonX orchestration

