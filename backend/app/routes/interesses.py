"""routes/interesses.py — Endpoints de interesses mútuos."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.interest import Interest, InterestStatus, InterestType
from app.models import Volunteer, Need
from app.schemas import InterestCreate, InterestRead

router = APIRouter(prefix="/interesses", tags=["Interesses"])


@router.post("/", response_model=InterestRead, status_code=status.HTTP_201_CREATED)
def create_interest(interest: InterestCreate, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.id == interest.volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Voluntário não encontrado.")

    need = db.query(Need).filter(Need.id == interest.need_id).first()
    if not need:
        raise HTTPException(status_code=404, detail="Necessidade não encontrada.")

    existing = db.query(Interest).filter(
        Interest.volunteer_id == interest.volunteer_id,
        Interest.need_id == interest.need_id,
        Interest.type == interest.type,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Interesse já registrado.")

    db_interest = Interest(**interest.model_dump())

    opposite_type = (
        InterestType.INSTITUTION_TO_VOLUNTEER
        if interest.type == InterestType.VOLUNTEER_TO_NEED
        else InterestType.VOLUNTEER_TO_NEED
    )
    opposite = db.query(Interest).filter(
        Interest.volunteer_id == interest.volunteer_id,
        Interest.need_id == interest.need_id,
        Interest.type == opposite_type,
    ).first()

    if opposite:
        setattr(db_interest, "status", InterestStatus.MUTUAL.value)
        setattr(opposite, "status", InterestStatus.MUTUAL.value)

    db.add(db_interest)
    if opposite:
        db.add(opposite)
    db.commit()
    db.refresh(db_interest)
    return db_interest


@router.get("/", response_model=List[InterestRead])
def list_interests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Interest).offset(skip).limit(limit).all()