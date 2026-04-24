"""
routes/institutions.py — Endpoints CRUD de instituições.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Institution
from app.schemas import InstitutionCreate, InstitutionUpdate, InstitutionRead

router = APIRouter(prefix="/institutions", tags=["Instituições"])


@router.post("/", response_model=InstitutionRead, status_code=status.HTTP_201_CREATED)
def create_institution(institution: InstitutionCreate, db: Session = Depends(get_db)):
    """Cria uma nova instituição."""
    existing = db.query(Institution).filter(Institution.email == institution.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    db_institution = Institution(**institution.model_dump())
    db.add(db_institution)
    db.commit()
    db.refresh(db_institution)
    return db_institution


@router.get("/", response_model=List[InstitutionRead])
def list_institutions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista instituições."""
    return db.query(Institution).offset(skip).limit(limit).all()


@router.get("/{institution_id}", response_model=InstitutionRead)
def get_institution(institution_id: int, db: Session = Depends(get_db)):
    """Busca uma instituição pelo ID."""
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(status_code=404, detail="Instituição não encontrada.")
    return institution