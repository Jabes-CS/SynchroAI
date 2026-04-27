"""
alert.py — Modelo de alertas de bem-estar.
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class AlertType(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    EMERGENCY = "emergency"
    WELLBEING = "wellbeing"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=False)
    volunteer = relationship("Volunteer", backref="alerts")
    message = Column(String(500), nullable=False)
    type = Column(Enum(AlertType), default=AlertType.INFO, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Alert id={self.id} volunteer={self.volunteer_id} type={self.type.value}>"