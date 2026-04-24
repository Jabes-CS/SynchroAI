"""
need.py — Modelo da tabela 'needs'.

Representa uma necessidade/demanda cadastrada por uma instituição.
Ex: "Precisamos de 5 enfermeiros no abrigo X amanhã às 8h".
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class NeedStatus(str, enum.Enum):
    """Estados de uma necessidade."""
    OPEN = "open"              # Ainda procurando voluntários
    IN_PROGRESS = "in_progress"  # Voluntários alocados, em execução
    COMPLETED = "completed"    # Concluída
    CANCELLED = "cancelled"    # Cancelada pela instituição


class UrgencyLevel(str, enum.Enum):
    """Níveis de urgência da necessidade."""
    LOW = "low"                # Pode esperar dias
    MEDIUM = "medium"          # Alguns dias
    HIGH = "high"              # Mesmo dia / próximas horas
    CRITICAL = "critical"      # Emergência imediata


class Need(Base):
    __tablename__ = "needs"

    # ========== Identificação ==========
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    # ========== Relacionamento com instituição ==========
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    institution = relationship("Institution", backref="needs")

    # ========== Requisitos ==========
    required_skills = Column(JSON, default=list)   # ["enfermagem", "direção"]
    volunteers_needed = Column(Integer, default=1)
    urgency = Column(Enum(UrgencyLevel), default=UrgencyLevel.MEDIUM)

    # ========== Localização da ação ==========
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)
    address = Column(String(300), nullable=True)

    # ========== Janela de atuação ==========
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)

    # ========== Estado ==========
    status = Column(Enum(NeedStatus), default=NeedStatus.OPEN, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Need id={self.id} title='{self.title}' status={self.status.value}>"