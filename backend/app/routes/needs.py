"""
routes/needs.py — Endpoints CRUD de necessidades.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Need, Institution, Match, MatchStatus
from app.schemas import NeedCreate, NeedUpdate, NeedRead

router = APIRouter(prefix="/needs", tags=["Necessidades"])


@router.get("/{need_id}/volunteers")
def get_need_volunteers(need_id: int, db: Session = Depends(get_db)):
    """Retorna voluntários vinculados a uma necessidade concluída."""
    need = db.query(Need).filter(Need.id == need_id).first()
    if not need:
        raise HTTPException(status_code=404, detail="Necessidade não encontrada.")

    completed_matches = (
        db.query(Match)
        .filter(Match.need_id == need_id, Match.status == MatchStatus.COMPLETED)
        .all()
    )

    volunteers = []
    for match in completed_matches:
        volunteer = match.volunteer
        if volunteer:
            volunteers.append(
                {
                    "id": volunteer.id,
                    "name": volunteer.name,
                    "email": volunteer.email,
                    "skills": volunteer.skills or [],
                }
            )

    return {
        "need_id": need_id,
        "need_title": need.title,
        "volunteers": volunteers,
    }


@router.post("/", response_model=NeedRead, status_code=status.HTTP_201_CREATED)
def create_need(need: NeedCreate, db: Session = Depends(get_db)):
    """Cria uma nova necessidade (vinculada a uma instituição)."""
    # Valida se a instituição existe
    institution = db.query(Institution).filter(Institution.id == need.institution_id).first()
    if not institution:
        raise HTTPException(status_code=404, detail="Instituição não encontrada.")

    db_need = Need(**need.model_dump())
    db.add(db_need)
    db.commit()
    db.refresh(db_need)
    return db_need


@router.get("/", response_model=List[NeedRead])
def list_needs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista necessidades."""
    return db.query(Need).offset(skip).limit(limit).all()


@router.get("/{need_id}", response_model=NeedRead)
def get_need(need_id: int, db: Session = Depends(get_db)):
    """Busca uma necessidade pelo ID."""
    need = db.query(Need).filter(Need.id == need_id).first()
    if not need:
        raise HTTPException(status_code=404, detail="Necessidade não encontrada.")
    return need


@router.patch("/{need_id}", response_model=NeedRead)
def patch_need(need_id: int, need_update: NeedUpdate, db: Session = Depends(get_db)):
    """Atualiza parcialmente os dados de uma necessidade."""
    need = db.query(Need).filter(Need.id == need_id).first()
    if not need:
        raise HTTPException(status_code=404, detail="Necessidade não encontrada.")

    update_data = need_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(need, field, value)

    db.commit()
    db.refresh(need)
    return need


@router.delete("/{need_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_need(need_id: int, db: Session = Depends(get_db)):
    """Deleta uma necessidade."""
    need = db.query(Need).filter(Need.id == need_id).first()
    if not need:
        raise HTTPException(status_code=404, detail="Necessidade não encontrada.")
    db.delete(need)
    db.commit()
    return None