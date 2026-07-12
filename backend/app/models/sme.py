from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class SME(Base):
    __tablename__ = "smes"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    legal_name = Column(String(255), index=True, nullable=False)
    industry = Column(String(100), index=True, nullable=True)
    business_age_months = Column(Integer, nullable=True)
    ownership_type = Column(String(100), nullable=True)
    registration_date = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False, default="active")
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = relationship("Organization", back_populates="smes")
    assessments = relationship("Assessment", back_populates="sme")
