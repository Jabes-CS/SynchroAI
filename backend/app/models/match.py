"""
match.py — Modelo da tabela 'matches'.

Representa um pareamento entre um voluntário e uma necessidade.
O agente Pareador do watsonx cria estes matches, e o voluntário
pode aceitar ou recusar.
"""

from sqlalchemy import Column, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class MatchStatus(str, enum.Enum):
    """Estados possíveis de um match."""
    SUGGESTED = "suggested"    # IA sugeriu, aguardando resposta
    ACCEPTED = "accepted"      # Voluntário aceitou
    REJECTED = "rejected"      # Voluntário recusou
    COMPLETED = "completed"    # Atividade realizada
    NO_SHOW = "no_show"       # Voluntário aceitou mas não compareceu


class Match(Base):
    __tablename__ = "matches"

    # ========== Identificação ==========
    id = Column(Integer, primary_key=True, index=True)

    # ========== Relacionamentos ==========
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=False)
    volunteer = relationship("Volunteer", backref="matches")

    need_id = Column(Integer, ForeignKey("needs.id"), nullable=False)
    need = relationship("Need", backref="matches")

    # ========== Qualidade do match ==========
    score = Column(Float, default=0.0)  # 0.0 a 100.0 — quão bom é o match

    # ========== Estado ==========
    status = Column(Enum(MatchStatus), default=MatchStatus.SUGGESTED, nullable=False)

    # ========== Timestamps ==========
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    responded_at = Column(DateTime(timezone=True), nullable=True)  # Quando aceitou/recusou

    def __repr__(self):
        return f"<Match id={self.id} volunteer={self.volunteer_id} need={self.need_id} score={self.score}>"