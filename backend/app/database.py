"""
database.py — Configuração central de conexão com o banco de dados.

Este arquivo é o coração do backend. Ele:
  1. Carrega a URL do banco do .env
  2. Cria o "engine" (motor de conexão SQLAlchemy)
  3. Cria a "SessionLocal" (fábrica de sessões para cada request)
  4. Expõe a "Base" que todos os modelos herdam
  5. Fornece o "get_db()" como dependência do FastAPI
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ============================================
# 1. CARREGAR VARIÁVEIS DE AMBIENTE
# ============================================
# Lê o arquivo .env e disponibiliza as variáveis via os.getenv()
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL não encontrada no .env. "
        "Verifique o arquivo backend/.env"
    )

# ============================================
# 2. CRIAR O ENGINE (MOTOR DE CONEXÃO)
# ============================================
# O engine é o objeto responsável por gerenciar o pool de conexões
# com o PostgreSQL. Ele é criado UMA vez e reutilizado.
engine = create_engine(
    DATABASE_URL,
    echo=False,          # True = imprime todo SQL no terminal (útil pra debug)
    pool_pre_ping=True,  # Verifica se a conexão está viva antes de usar
)

# ============================================
# 3. CRIAR A FÁBRICA DE SESSÕES
# ============================================
# Cada request do FastAPI abre uma sessão nova para falar com o banco
# e fecha ao terminar. Isso evita vazamento de conexões.
SessionLocal = sessionmaker(
    autocommit=False,   # Precisamos chamar commit() explicitamente
    autoflush=False,    # Não envia mudanças automaticamente ao banco
    bind=engine,        # Conecta a fábrica ao nosso engine
)

# ============================================
# 4. BASE DOS MODELOS
# ============================================
# Todos os modelos (Volunteer, Institution, etc.) vão herdar desta Base.
# É ela quem permite ao SQLAlchemy criar as tabelas no banco.
Base = declarative_base()


# ============================================
# 5. DEPENDÊNCIA DO FASTAPI PARA OBTER A SESSÃO
# ============================================
def get_db():
    """
    Dependência do FastAPI que fornece uma sessão do banco para cada request.

    Uso nos endpoints:
        @app.get("/volunteers")
        def list_volunteers(db: Session = Depends(get_db)):
            return db.query(Volunteer).all()

    O "yield" entrega a sessão ao endpoint, e o "finally" garante
    que ela será fechada ao fim do request — mesmo se der erro.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()