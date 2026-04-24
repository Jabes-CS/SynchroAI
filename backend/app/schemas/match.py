"""
schemas/match.py — Schemas Pydantic para Matches.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

from app.models.match import MatchStatus


class MatchBase(BaseModel):
    volunteer_id: int
    need_id: int
    score: float = Field(default=0.0, ge=0.0, le=100.0)


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    status: Optional[MatchStatus] = None


class MatchRead(MatchBase):
    id: int
    status: MatchStatus
    created_at: datetime
    responded_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)