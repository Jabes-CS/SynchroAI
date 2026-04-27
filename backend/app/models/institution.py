"""
institution.py — Modelo da tabela 'institutions'.

Representa uma organização que recebe apoio de voluntários.
Ex: ONGs, prefeituras, defesa civil, igrejas, comitês de crise.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum

from app.database import Base


class InstitutionType(str, enum.Enum):
    """Tipos de instituição que podem requisitar voluntários."""
    NGO = "ngo"                       # ONG
    GOVERNMENT = "government"         # Prefeitura, defesa civil
    RELIGIOUS = "religious"           # Igrejas, templos
    HEALTH = "health"                 # Hospitais, clínicas
    CRISIS_COMMITTEE = "crisis"       # Comitês de emergência
    OTHER = "other"


class Institution(Base):
    __tablename__ = "institutions"

    # ========== Identificação ==========
    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(18), unique=True, nullable=False, index=True)  # Formato: "12345678000199" ou "12.345.678/0001-99"
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(256), nullable=False)  # Hash da senha para autenticação

    # ========== Tipo ==========
    type = Column(
        Enum(InstitutionType),
        default=InstitutionType.NGO,
        nullable=False,
    )

    # ========== Localização ==========
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)
    address = Column(String(300), nullable=True)

    # ========== Controle ==========
    is_verified = Column(Boolean, default=False)   # Instituição validada pela equipe
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Institution id={self.id} name='{self.name}' type={self.type.value}>"