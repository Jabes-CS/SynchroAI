"""
schemas/institution.py — Schemas Pydantic para Instituições.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

from app.models.institution import InstitutionType


class InstitutionBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    type: InstitutionType = Field(default=InstitutionType.NGO)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=2)
    address: Optional[str] = Field(None, max_length=300)


class InstitutionCreate(InstitutionBase):
    pass


class InstitutionUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class InstitutionRead(InstitutionBase):
    id: int
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)