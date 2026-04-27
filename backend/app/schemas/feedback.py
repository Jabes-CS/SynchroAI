from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FeedbackCreate(BaseModel):
    volunteer_id: int
    need_id: int
    text: str
    rating: int


class FeedbackRead(FeedbackCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)