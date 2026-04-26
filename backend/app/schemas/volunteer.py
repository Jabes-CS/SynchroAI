"""
schemas/volunteer.py — Schemas Pydantic para Voluntários.

Define como os dados entram (POST, PUT) e saem (GET) da API.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.models.volunteer import VolunteerType


# ============================================
# SCHEMA BASE — campos compartilhados
# ============================================
class VolunteerBase(BaseModel):
    """Campos compartilhados entre criação e leitura."""
    name: str = Field(..., min_length=2, max_length=200, description="Nome completo")
    email: EmailStr = Field(..., description="Email único do voluntário")
    phone: Optional[str] = Field(None, max_length=20)
    type: VolunteerType = Field(default=VolunteerType.FREELANCER)
    skills: List[str] = Field(default_factory=list, description="Lista de habilidades")
    availability: Dict[str, Any] = Field(default_factory=dict)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=2)
    open_to_rotation: bool = True


# ============================================
# SCHEMA DE CRIAÇÃO — o que chega via POST /volunteers
# ============================================
class VolunteerCreate(VolunteerBase):
    """Dados necessários para CRIAR um voluntário."""
    pass  # Herda todos os campos de VolunteerBase


# ============================================
# SCHEMA DE ATUALIZAÇÃO — o que chega via PUT /volunteers/{id}
# ============================================
class VolunteerUpdate(BaseModel):
    """Todos os campos opcionais — atualização parcial."""
    name: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[Dict[str, Any]] = None
    city: Optional[str] = None
    state: Optional[str] = None
    open_to_rotation: Optional[bool] = None
    is_active: Optional[bool] = None
    points: Optional[int] = None  


# ============================================
# SCHEMA DE LEITURA — o que a API retorna
# ============================================
class VolunteerRead(VolunteerBase):
    """Dados retornados ao consultar um voluntário."""
    id: int
    points: int
    carfo_profile: Optional[Dict[str, Any]] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Permite criar o schema a partir de um objeto SQLAlchemy
    model_config = ConfigDict(from_attributes=True)