"""routes/feedbacks.py — Endpoints de feedback pós-missão."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Feedback, Volunteer, Need
from app.schemas import FeedbackCreate, FeedbackRead

router = APIRouter(prefix="/feedbacks", tags=["Feedbacks"])


@router.post("/", response_model=FeedbackRead, status_code=status.HTTP_201_CREATED)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.id == feedback.volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Voluntário não encontrado.")

    need = db.query(Need).filter(Need.id == feedback.need_id).first()
    if not need:
        raise HTTPException(status_code=404, detail="Necessidade não encontrada.")

    db_feedback = Feedback(**feedback.model_dump())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@router.get("/", response_model=List[FeedbackRead])
def list_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Feedback).offset(skip).limit(limit).all()