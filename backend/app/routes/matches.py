"""
routes/matches.py — Endpoints CRUD de matches.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Match, Volunteer, Need
from app.schemas import MatchCreate, MatchUpdate, MatchRead

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/", response_model=MatchRead, status_code=status.HTTP_201_CREATED)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    """Cria um novo match (geralmente feito pelo agente Pareador)."""
    # Valida voluntário e necessidade
    if not db.query(Volunteer).filter(Volunteer.id == match.volunteer_id).first():
        raise HTTPException(status_code=404, detail="Voluntário não encontrado.")
    if not db.query(Need).filter(Need.id == match.need_id).first():
        raise HTTPException(status_code=404, detail="Necessidade não encontrada.")

    db_match = Match(**match.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.get("/", response_model=List[MatchRead])
def list_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista matches."""
    return db.query(Match).offset(skip).limit(limit).all()


@router.get("/{match_id}", response_model=MatchRead)
def get_match(match_id: int, db: Session = Depends(get_db)):
    """Busca um match pelo ID."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match não encontrado.")
    return match

@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    """Deleta um match."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match não encontrado.")
    db.delete(match)
    db.commit()
    return None