"""
interest.py — Modelo de interesses mútuos entre voluntários e necessidades.
"""

from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class InterestType(str, enum.Enum):
    VOLUNTEER_TO_NEED = "voluntario_para_necessidade"
    INSTITUTION_TO_VOLUNTEER = "instituicao_para_voluntario"


class InterestStatus(str, enum.Enum):
    PENDING = "pending"
    MUTUAL = "mutual"


class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=False)
    volunteer = relationship("Volunteer", backref="interests")
    need_id = Column(Integer, ForeignKey("needs.id"), nullable=False)
    need = relationship("Need", backref="interests")
    type = Column(Enum(InterestType), nullable=False)
    status = Column(Enum(InterestStatus), default=InterestStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Interest id={self.id} volunteer={self.volunteer_id} need={self.need_id} type={self.type.value} status={self.status.value}>"