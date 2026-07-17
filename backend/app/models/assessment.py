from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    sme_id = Column(Integer, ForeignKey("smes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_version = Column(String(100), nullable=True)
    risk_score = Column(Float, nullable=False)
    risk_category = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="completed")
    features_json = Column(JSON, nullable=False)
    shap_values_json = Column(JSON, nullable=False)
    recommendations_json = Column(JSON, nullable=True)
    ai_insights = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sme = relationship("SME", back_populates="assessments")
    analyst = relationship("User", back_populates="assessments")
    predictions = relationship("Prediction", back_populates="assessment", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="assessment", cascade="all, delete-orphan")
    histories = relationship("AssessmentHistory", back_populates="assessment", cascade="all, delete-orphan")