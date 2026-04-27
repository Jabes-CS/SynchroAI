"""
database.py — Configuração central de conexão com o banco de dados.

Suporta tanto desenvolvimento local (PostgreSQL local) quanto produção (Render).
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Em produção (Render), usa DATABASE_URL.
# Localmente, também usa DATABASE_URL.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL não encontrada no ambiente. "
        "Verifique o arquivo .env localmente ou as variáveis de ambiente em produção."
    )

# Configuração de conexão — adiciona SSL se for banco do Render
connect_args = {}
if "render.com" in DATABASE_URL:
    connect_args = {"sslmode": "require"}

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """
    Dependência FastAPI que fornece uma sessão do banco para cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()