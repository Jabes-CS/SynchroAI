"""routes/alertas.py — Endpoints de alertas de bem-estar."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Alert, Volunteer
from app.schemas import AlertCreate, AlertRead

router = APIRouter(prefix="/alertas", tags=["Alertas"])


@router.post("/", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.id == alert.volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Voluntário não encontrado.")

    db_alert = Alert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.get("/", response_model=List[AlertRead])
def list_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Alert).offset(skip).limit(limit).all()