"""
routes/institutions.py — Endpoints CRUD de instituições.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Institution
from app.schemas import InstitutionCreate, InstitutionUpdate, InstitutionRead

router = APIRouter(prefix="/institutions", tags=["Instituições"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/", response_model=InstitutionRead, status_code=status.HTTP_201_CREATED)
def create_institution(institution: InstitutionCreate, db: Session = Depends(get_db)):
    """Cria uma nova instituição."""
    existing_email = db.query(Institution).filter(Institution.email == institution.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    existing_cnpj = db.query(Institution).filter(Institution.cnpj == institution.cnpj).first()
    if existing_cnpj:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado.")

    institution_data = institution.model_dump(exclude={"password"})
    institution_data["password_hash"] = hash_password(institution.password) if institution.password else ""

    db_institution = Institution(**institution_data)
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


@router.get("/cnpj/{cnpj}", response_model=InstitutionRead)
def get_institution_by_cnpj(cnpj: str, db: Session = Depends(get_db)):
    """Busca uma instituição pelo CNPJ."""
    cnpj_normalized = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    institution = db.query(Institution).filter(Institution.cnpj == cnpj_normalized).first()
    if not institution:
        raise HTTPException(status_code=404, detail="Instituição não encontrada.")
    return institution


def _apply_update_to_institution(institution: Institution, update_data: dict) -> Institution:
    for field, value in update_data.items():
        setattr(institution, field, value)
    return institution


@router.patch("/{institution_id}", response_model=InstitutionRead)
def patch_institution(
    institution_id: int,
    institution_update: InstitutionUpdate,
    db: Session = Depends(get_db),
):
    """Atualiza parcialmente os dados de uma instituição."""
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(status_code=404, detail="Instituição não encontrada.")

    update_data = institution_update.model_dump(exclude_unset=True)
    _apply_update_to_institution(institution, update_data)
    db.commit()
    db.refresh(institution)
    return institution


@router.put("/{institution_id}", response_model=InstitutionRead)
def update_institution(
    institution_id: int,
    institution_update: InstitutionUpdate,
    db: Session = Depends(get_db),
):
    """Atualiza dados de uma instituição."""
    return patch_institution(institution_id, institution_update, db)


@router.post("/verify-password")
def verify_institution_password(payload: dict, db: Session = Depends(get_db)):
    """Verifica a senha de uma instituição pelo CNPJ."""
    cnpj = payload.get("cnpj")
    password = payload.get("password")
    if not cnpj or not password:
        raise HTTPException(status_code=400, detail="CNPJ e senha são obrigatórios.")

    cnpj_normalized = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    institution = db.query(Institution).filter(Institution.cnpj == cnpj_normalized).first()
    if not institution:
        raise HTTPException(status_code=404, detail="Instituição não encontrada.")

    if not verify_password(password, institution.password_hash):
        raise HTTPException(status_code=401, detail="Senha incorreta.")

    return {
        "institution_id": institution.id,
        "name": institution.name,
    }


@router.post("/request-password-reset")
def request_password_reset(payload: dict, db: Session = Depends(get_db)):
    """Simula solicitação de recuperação de senha para uma instituição."""
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email é obrigatório.")

    institution = db.query(Institution).filter(Institution.email == email).first()
    if not institution:
        raise HTTPException(status_code=404, detail="Email não encontrado.")

    return {"email_sent": True, "message": "Instruções de recuperação enviadas por email."}


@router.delete("/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_institution(institution_id: int, db: Session = Depends(get_db)):
    """Deleta uma instituição."""
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(status_code=404, detail="Instituição não encontrada.")
    db.delete(institution)
    db.commit()
    return None