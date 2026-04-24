"""
reward.py — Modelo da tabela 'rewards'.

Registra os bônus/recompensas que os voluntários resgataram
usando seus pontos acumulados. Base do sistema de retenção.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class RewardType(str, enum.Enum):
    """Tipos de recompensa disponíveis."""
    LEISURE = "leisure"              # Ingressos, vouchers de lazer
    MAINTENANCE = "maintenance"      # Vale-alimentação, transporte
    COURSE = "course"                # Cursos e capacitação
    MERCHANDISE = "merchandise"      # Camisetas, brindes
    OTHER = "other"


class Reward(Base):
    __tablename__ = "rewards"

    # ========== Identificação ==========
    id = Column(Integer, primary_key=True, index=True)

    # ========== Relacionamento ==========
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=False)
    volunteer = relationship("Volunteer", backref="rewards")

    # ========== Dados da recompensa ==========
    type = Column(Enum(RewardType), default=RewardType.OTHER, nullable=False)
    description = Column(String(300), nullable=False)
    points_spent = Column(Integer, nullable=False)

    # ========== Timestamps ==========
    redeemed_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Reward id={self.id} volunteer={self.volunteer_id} type={self.type.value}>"