from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AlertCreate(BaseModel):
    volunteer_id: int
    message: str
    type: str


class AlertRead(AlertCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)