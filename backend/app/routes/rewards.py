"""routes/rewards.py — Endpoints para processar pontos e badges."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Need, Volunteer
from app.models.need import UrgencyLevel

router = APIRouter(prefix="/rewards", tags=["Recompensas"])


class Evaluation(BaseModel):
    volunteer_id: int
    nota: float
    feedback: Optional[str] = None
    horas_trabalhadas: Optional[float] = None


class RewardProcessRequest(BaseModel):
    need_id: int
    avaliacoes: List[Evaluation]


@router.post("/processar")
def process_rewards(request: RewardProcessRequest, db: Session = Depends(get_db)):
    """Processa pontuação e atualiza os pontos dos voluntários."""
    need = db.query(Need).filter(Need.id == request.need_id).first()
    if not need:
        raise HTTPException(status_code=404, detail="Necessidade não encontrada.")

    urgency_multiplier = {
        UrgencyLevel.CRITICAL: 3.0,
        UrgencyLevel.HIGH: 2.0,
        UrgencyLevel.MEDIUM: 1.0,
        UrgencyLevel.LOW: 0.5,
    }

    bonus_by_rating = {
        5: 20,
        4: 10,
        3: 0,
        2: -5,
        1: -10,
    }

    multiplier = urgency_multiplier.get(need.urgency, 1.0)
    recompensas = []
    novos_badges = []

    for evaluation in request.avaliacoes:
        volunteer = db.query(Volunteer).filter(Volunteer.id == evaluation.volunteer_id).first()
        if not volunteer:
            raise HTTPException(
                status_code=404,
                detail=f"Voluntário {evaluation.volunteer_id} não encontrado.",
            )

        horas = evaluation.horas_trabalhadas if evaluation.horas_trabalhadas else 1.0
        nota_int = int(round(evaluation.nota))
        bonus = bonus_by_rating.get(nota_int, 0)
        earned = int(max(0, horas * multiplier + bonus))
        previous_points = volunteer.points
        volunteer.points += earned

        badge = None
        if previous_points < 50 <= volunteer.points:
            badge = "Iniciante"
        elif previous_points < 200 <= volunteer.points:
            badge = "Engajado"
        elif previous_points < 500 <= volunteer.points:
            badge = "Comprometido"
        elif previous_points < 1000 <= volunteer.points:
            badge = "Embaixador"

        if badge:
            novos_badges.append({"volunteer_id": volunteer.id, "badge": badge})

        recompensas.append(
            {
                "volunteer_id": volunteer.id,
                "name": volunteer.name,
                "points_awarded": earned,
                "total_points": volunteer.points,
                "badge_awarded": badge,
                "feedback_received": evaluation.feedback,
            }
        )

    db.commit()

    return {
        "processado": True,
        "recompensas": recompensas,
        "badges": novos_badges,
    }
