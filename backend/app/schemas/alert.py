from pydantic import BaseModel
from datetime import datetime


class AlertCreate(BaseModel):
    title: str
    description: str


class AlertRead(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime