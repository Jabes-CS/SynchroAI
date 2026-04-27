from pydantic import BaseModel
from datetime import datetime

class FeedbackCreate(BaseModel):
    content: str
    rating: int

class FeedbackRead(BaseModel):
    id: int
    content: str
    rating: int
    created_at: datetime