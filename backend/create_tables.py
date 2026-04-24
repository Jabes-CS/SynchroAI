"""
create_tables.py — Script para criar todas as tabelas no banco.

Execute este script UMA VEZ para popular o banco com as tabelas.
Depois disso, o próprio Alembic (migrations) gerencia alterações.
"""

from app.database import engine, Base

# IMPORTANTE: importar os modelos faz o SQLAlchemy "enxergar" eles
from app.models import (
    Volunteer,
    Institution,
    Need,
    Match,
    TaskHistory,
    Reward,
)

print("🔨 Criando tabelas no banco synchroai...")

Base.metadata.create_all(bind=engine)

print("✅ Tabelas criadas com sucesso!")
print("\nTabelas no banco:")
for table_name in Base.metadata.tables.keys():
    print(f"  - {table_name}")