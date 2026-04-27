"""
feedback.py — Modelo de feedbacks pós-missão.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=False)
    volunteer = relationship("Volunteer", backref="feedbacks")
    need_id = Column(Integer, ForeignKey("needs.id"), nullable=False)
    need = relationship("Need", backref="feedbacks")
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Feedback id={self.id} volunteer={self.volunteer_id} need={self.need_id} rating={self.rating}>"