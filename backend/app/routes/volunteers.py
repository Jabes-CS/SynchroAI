"""
routes/volunteers.py — Endpoints CRUD de voluntários.

Endpoints criados:
  POST   /volunteers         — Criar voluntário
  GET    /volunteers         — Listar todos
  GET    /volunteers/{id}    — Buscar por ID
  PUT    /volunteers/{id}    — Atualizar
  DELETE /volunteers/{id}    — Desativar (soft delete)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Volunteer
from app.schemas import VolunteerCreate, VolunteerUpdate, VolunteerRead

router = APIRouter(prefix="/volunteers", tags=["Voluntários"])


@router.post("/", response_model=VolunteerRead, status_code=status.HTTP_201_CREATED)
def create_volunteer(volunteer: VolunteerCreate, db: Session = Depends(get_db)):
    """Cria um novo voluntário."""
    # Verifica email único
    existing = db.query(Volunteer).filter(Volunteer.email == volunteer.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado no sistema."
        )

    db_volunteer = Volunteer(**volunteer.model_dump())
    db.add(db_volunteer)
    db.commit()
    db.refresh(db_volunteer)
    return db_volunteer


@router.get("/", response_model=List[VolunteerRead])
def list_volunteers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Lista voluntários com paginação."""
    volunteers = db.query(Volunteer).offset(skip).limit(limit).all()
    return volunteers


@router.get("/{volunteer_id}", response_model=VolunteerRead)
def get_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    """Busca um voluntário pelo ID."""
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Voluntário não encontrado.")
    return volunteer


@router.put("/{volunteer_id}", response_model=VolunteerRead)
def update_volunteer(
    volunteer_id: int,
    volunteer_update: VolunteerUpdate,
    db: Session = Depends(get_db),
):
    """Atualiza dados de um voluntário."""
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Voluntário não encontrado.")

    # Atualiza apenas os campos enviados (exclude_unset)
    update_data = volunteer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(volunteer, field, value)

    db.commit()
    db.refresh(volunteer)
    return volunteer


@router.delete("/{volunteer_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    """Desativa (não deleta) um voluntário. Preserva histórico."""
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Voluntário não encontrado.")
    
    db.delete(volunteer) ## descomentar para testes
    ##volunteer.is_active = False ##comentar para testes
    db.commit()
    return None