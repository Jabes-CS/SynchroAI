"""
create_tables_prod.py — Cria tabelas no banco de PRODUÇÃO (Render).

Use APENAS uma vez para popular o banco do Render com as tabelas.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# Pega a URL do banco de PRODUÇÃO
DATABASE_URL_PROD = os.getenv("DATABASE_URL_PROD")

if not DATABASE_URL_PROD:
    raise RuntimeError("DATABASE_URL_PROD não encontrada no .env")

# Cria engine apontando pro Render
engine = create_engine(DATABASE_URL_PROD)

# Importa Base e modelos
from app.database import Base
from app.models import (
    Volunteer,
    Institution,
    Need,
    Match,
    TaskHistory,
    Reward,
)

print("🔨 Criando tabelas no banco de PRODUÇÃO (Render)...")
print(f"   URL: {DATABASE_URL_PROD[:50]}...")

Base.metadata.create_all(bind=engine)

print("\n✅ Tabelas criadas com sucesso no Render!")
print("\nTabelas criadas:")
for table_name in Base.metadata.tables.keys():
    print(f"  - {table_name}")