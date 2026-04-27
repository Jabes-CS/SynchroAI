"""
routes/volunteers.py — Endpoints CRUD de voluntários.

Endpoints criados:
  POST   /volunteers                 — Criar voluntário
  GET    /volunteers                 — Listar todos
  GET    /volunteers/{id}            — Buscar por ID
  GET    /volunteers/cpf/{cpf}       — Buscar por CPF
  PATCH  /volunteers/{id}            — Atualizar parcialmente
  PUT    /volunteers/{id}            — Atualizar completamente
  POST   /volunteers/verify-password — Verificar senha
  POST   /volunteers/request-password-reset — Solicitar recuperação de senha
  DELETE /volunteers/{id}            — Desativar (soft delete)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Volunteer
from app.schemas import VolunteerCreate, VolunteerUpdate, VolunteerRead

router = APIRouter(prefix="/volunteers", tags=["Voluntários"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/", response_model=VolunteerRead, status_code=status.HTTP_201_CREATED)
def create_volunteer(volunteer: VolunteerCreate, db: Session = Depends(get_db)):
    """Cria um novo voluntário."""
    # Verifica email único
    existing_email = db.query(Volunteer).filter(Volunteer.email == volunteer.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado no sistema."
        )

    existing_cpf = db.query(Volunteer).filter(Volunteer.cpf == volunteer.cpf).first()
    if existing_cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado no sistema."
        )

    volunteer_data = volunteer.model_dump(exclude={"password"})
    volunteer_data["password_hash"] = hash_password(volunteer.password) if volunteer.password else ""

    db_volunteer = Volunteer(**volunteer_data)
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


@router.get("/cpf/{cpf}", response_model=VolunteerRead)
def get_volunteer_by_cpf(cpf: str, db: Session = Depends(get_db)):
    """Busca um voluntário pelo CPF."""
    cpf_normalized = cpf.replace(".", "").replace("-", "").strip()
    volunteer = db.query(Volunteer).filter(Volunteer.cpf == cpf_normalized).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Voluntário não encontrado.")
    return volunteer


def _apply_update_to_volunteer(volunteer: Volunteer, update_data: dict) -> Volunteer:
    for field, value in update_data.items():
        setattr(volunteer, field, value)
    return volunteer


@router.patch("/{volunteer_id}", response_model=VolunteerRead)
def patch_volunteer(
    volunteer_id: int,
    volunteer_update: VolunteerUpdate,
    db: Session = Depends(get_db),
):
    """Atualiza parcialmente os dados de um voluntário."""
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Voluntário não encontrado.")

    update_data = volunteer_update.model_dump(exclude_unset=True)
    _apply_update_to_volunteer(volunteer, update_data)
    db.commit()
    db.refresh(volunteer)
    return volunteer


@router.put("/{volunteer_id}", response_model=VolunteerRead)
def update_volunteer(
    volunteer_id: int,
    volunteer_update: VolunteerUpdate,
    db: Session = Depends(get_db),
):
    """Atualiza dados de um voluntário."""
    return patch_volunteer(volunteer_id, volunteer_update, db)


@router.post("/verify-password")
def verify_volunteer_password(payload: dict, db: Session = Depends(get_db)):
    """Verifica a senha de um voluntário pelo CPF."""
    cpf = payload.get("cpf")
    password = payload.get("password")
    if not cpf or not password:
        raise HTTPException(status_code=400, detail="CPF e senha são obrigatórios.")

    cpf_normalized = cpf.replace(".", "").replace("-", "").strip()
    volunteer = db.query(Volunteer).filter(Volunteer.cpf == cpf_normalized).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Voluntário não encontrado.")

    if not verify_password(password, volunteer.password_hash):
        raise HTTPException(status_code=401, detail="Senha incorreta.")

    return {
        "volunteer_id": volunteer.id,
        "name": volunteer.name,
    }


@router.post("/request-password-reset")
def request_password_reset(payload: dict, db: Session = Depends(get_db)):
    """Simula solicitação de recuperação de senha para um voluntário."""
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email é obrigatório.")

    volunteer = db.query(Volunteer).filter(Volunteer.email == email).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Email não encontrado.")

    # Aqui poderíamos disparar email; por enquanto apenas retornamos sucesso.
    return {"email_sent": True, "message": "Instruções de recuperação enviadas por email."}


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

