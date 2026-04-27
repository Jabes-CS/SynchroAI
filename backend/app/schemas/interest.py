from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.interest import InterestType, InterestStatus


class InterestCreate(BaseModel):
    volunteer_id: int
    need_id: int
    type: InterestType


class InterestRead(InterestCreate):
    id: int
    status: InterestStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)