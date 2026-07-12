from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    report_type = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default="generated")
    file_url = Column(String(500), nullable=True)
    metadata = Column(JSON, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="reports")
