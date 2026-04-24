"""
schemas/need.py — Schemas Pydantic para Necessidades.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

from app.models.need import NeedStatus, UrgencyLevel


class NeedBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    institution_id: int
    required_skills: List[str] = Field(default_factory=list)
    volunteers_needed: int = Field(default=1, ge=1)
    urgency: UrgencyLevel = Field(default=UrgencyLevel.MEDIUM)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=2)
    address: Optional[str] = Field(None, max_length=300)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class NeedCreate(NeedBase):
    pass


class NeedUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    volunteers_needed: Optional[int] = None
    urgency: Optional[UrgencyLevel] = None
    status: Optional[NeedStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class NeedRead(NeedBase):
    id: int
    status: NeedStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)