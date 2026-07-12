from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class AssessmentHistory(Base):
    __tablename__ = "assessment_history"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    change_type = Column(String(100), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    changes = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="histories")
