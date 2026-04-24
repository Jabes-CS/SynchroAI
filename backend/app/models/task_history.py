"""
task_history.py — Modelo da tabela 'task_history'.

Registra cada atividade concluída por um voluntário.
É a base para o sistema de pontuação e análise de impacto.
"""

from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class TaskHistory(Base):
    __tablename__ = "task_history"

    # ========== Identificação ==========
    id = Column(Integer, primary_key=True, index=True)

    # ========== Relacionamento com o match original ==========
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    match = relationship("Match", backref="task_history")

    # ========== Dados da atividade ==========
    hours_worked = Column(Float, default=0.0)
    feedback_score = Column(Integer, nullable=True)  # 1 a 5 (avaliação da instituição)
    feedback_text = Column(Text, nullable=True)

    # ========== Pontos ganhos ==========
    points_earned = Column(Integer, default=0)

    # ========== Timestamps ==========
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TaskHistory id={self.id} match={self.match_id} points={self.points_earned}>"