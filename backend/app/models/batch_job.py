from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class BatchAssessmentJob(Base):
    __tablename__ = "batch_assessment_jobs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    total_rows = Column(Integer, nullable=True)
    processed_rows = Column(Integer, nullable=True, default=0)
    results_json = Column(JSON, nullable=True)
    error_message = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    organization = relationship("Organization", back_populates="batch_jobs")
    user = relationship("User", back_populates="batch_jobs")