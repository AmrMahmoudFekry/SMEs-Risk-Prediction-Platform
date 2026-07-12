from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    model_version = Column(String(100), nullable=False)
    probability = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    input_payload = Column(JSON, nullable=False)
    output_payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="predictions")
