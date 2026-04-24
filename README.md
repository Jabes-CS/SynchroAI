# 🤝 SynchroAI

> **Orquestrando voluntariado inteligente para situações de crise.**

Uma plataforma baseada em Inteligência Artificial que conecta voluntários e instituições de forma dinâmica, usando o **IBM watsonx Orchestrate** como núcleo de coordenação para maximizar o impacto social em cenários de desastre, emergência e alta vulnerabilidade.

---

## 📌 Sobre o Projeto

**SynchroAI** é uma solução desenvolvida para o **Hackathon IA Descomplicada: Da Ideia à Implementação (UNASP + IBM 2026)**, com o tema *"Orquestrando o Voluntariado Inteligente para Situações de Crise"*.

### 🌊 O Problema

Nas enchentes do **Rio Grande do Sul em 2024**, milhares de pessoas se voluntariaram para ajudar — mas a coordenação foi caótica:

- Médicos chegavam sem saber onde atuar
- Doações de roupas sobravam enquanto água faltava
- Voluntários qualificados eram alocados em tarefas simples, enquanto necessidades técnicas ficavam sem resposta
- Instituições tinham dificuldade em mapear, filtrar e coordenar voluntários eficientemente

Esses problemas não são exclusivos do RS. Eles se repetem em **toda crise humanitária** no Brasil e no mundo, resultando em desperdício de potencial humano e atrasos em respostas críticas.

### 💡 A Solução

O **SynchroAI** resolve isso através de uma arquitetura de **agentes de IA orquestrados**, que:

- 🎯 **Perfilam voluntários** automaticamente — extraindo habilidades, disponibilidade e contexto
- 🔗 **Pareiam necessidades e talentos** com precisão, priorizando urgência e proximidade
- 💚 **Protegem o bem-estar** dos voluntários com sistema de revezamento inteligente
- 🏆 **Incentivam a retenção** através de gamificação e bônus por impacto

---

## 🏗️ Arquitetura

Detalhes completos em [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md).

---



## 🤖 Agentes de IA

Cada agente tem uma responsabilidade bem definida dentro da orquestração:

| Agente | Função |
|--------|--------|
| **Perfilador** | Coleta habilidades, disponibilidade e perfil comportamental do voluntário |
| **Pareador** | Casa voluntários e necessidades baseado em skills, urgência e localização |
| **Bem-estar** | Gerencia revezamento entre voluntários para evitar burnout |
| **Pontuação** | Sistema de gamificação para retenção e reconhecimento |

Prompts e configurações em [`watsonx/agents/`](watsonx/agents/).

---

## 👥 Tipos de Voluntário

O SynchroAI reconhece que nem todo voluntário tem o mesmo perfil de engajamento:

- **🔵 Voluntário Permanente** — Atuação contínua, com tempo para cadastro completo e perfil comportamental (CARFO). Ideal para gestão de projetos de longo prazo.
- **🟢 Voluntário Freelancer** — Atuação por demanda ou emergência. Cadastro rápido e alocação imediata em tarefas específicas.

---

## 🛠️ Stack Tecnológica

### Backend
- **Python 3.11+**
- **FastAPI** — framework web assíncrono
- **SQLAlchemy** + **Alembic** — ORM e migrations
- **PostgreSQL** — banco de dados principal
- **Pydantic** — validação de dados

### Frontend
- **React 18** + **Vite**
- **JavaScript (ES6+)**
- **CSS Modules**

### Inteligência Artificial
- **IBM watsonx Orchestrate** — orquestração de agentes
- **IBM Granite** — modelo de linguagem

### Ferramentas
- **Git** + **GitHub** — controle de versão
- **VS Code** — IDE

---

## 🚀 Como Rodar Localmente

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Conta IBM Cloud com acesso ao watsonx Orchestrate

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
cp .env.example .env           # Preencha com suas credenciais

uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

A aplicação web estará disponível em `http://localhost:5173`.

---

## 📂 Estrutura do Projeto

---

## 👨‍💻 Equipe

**Equipe SynchroAI**

| Integrante | Papel | Contato |
|------------|-------|---------|
| **Jabes Candido** | Desenvolvimento Full-Stack e Arquitetura | [GitHub](https://github.com/Jabes-CS) |
| **Nickolas Bragato** | Desenvolvimento e Orquestração IA | — | [GitHub](https://github.com/Nickolas-Bragato) |

**Orientação:** UNASP — Centro Universitário Adventista de São Paulo
**Parceiro:** IBM

---

## 🎯 Status do Projeto

🟡 **Em desenvolvimento** — Hackathon IA Descomplicada 2026
📅 **Data de entrega:** 27 de Abril de 2026

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">
  <em>Feito com 💙 durante o Hackathon IA Descomplicada — UNASP + IBM 2026</em>
</p>
