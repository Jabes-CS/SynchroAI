"""
volunteer.py — Modelo da tabela 'volunteers'.

Representa um voluntário cadastrado no SynchroAI.
Dois tipos possíveis:
  - PERMANENT: voluntário fixo, com perfil completo (CARFO)
  - FREELANCER: voluntário por demanda, cadastro rápido
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, JSON
from sqlalchemy.sql import func
import enum

from app.database import Base


class VolunteerType(str, enum.Enum):
    """Tipos de voluntário no sistema."""
    PERMANENT = "permanent"       # Voluntário fixo, engajamento de longo prazo
    FREELANCER = "freelancer"     # Voluntário por demanda ou emergência


class Volunteer(Base):
    __tablename__ = "volunteers"

    # ========== Identificação ==========
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)

    # ========== Tipo e perfil ==========
    type = Column(
        Enum(VolunteerType),
        default=VolunteerType.FREELANCER,
        nullable=False,
    )
    skills = Column(JSON, default=list)           # ["enfermagem", "logística", ...]
    availability = Column(JSON, default=dict)      # {"seg": "18h-22h", ...}
    carfo_profile = Column(JSON, nullable=True)    # Perfil comportamental (só para PERMANENT)

    # ========== Localização ==========
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)       # Ex: "RS", "SP"
    latitude = Column(String(20), nullable=True)
    longitude = Column(String(20), nullable=True)

    # ========== Gamificação e bem-estar ==========
    points = Column(Integer, default=0)
    open_to_rotation = Column(Boolean, default=True)

    # ========== Controle ==========
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Volunteer id={self.id} name='{self.name}' type={self.type.value}>"