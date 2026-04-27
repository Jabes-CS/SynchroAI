from pydantic import BaseModel
from typing import Optional


class InterestCreate(BaseModel):
    name: str
    description: Optional[str] = None


class InterestRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None