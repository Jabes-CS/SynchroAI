"""
routes/needs.py — Endpoints CRUD de necessidades.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Need, Institution
from app.schemas import NeedCreate, NeedUpdate, NeedRead

router = APIRouter(prefix="/needs", tags=["Necessidades"])


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

@router.delete("/{need_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_need(need_id: int, db: Session = Depends(get_db)):
    """Deleta uma necessidade."""
    need = db.query(Need).filter(Need.id == need_id).first()
    if not need:
        raise HTTPException(status_code=404, detail="Necessidade não encontrada.")
    db.delete(need)
    db.commit()
    return None