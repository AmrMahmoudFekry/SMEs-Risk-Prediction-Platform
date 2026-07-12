from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class ReportVersion(Base):
    __tablename__ = "report_versions"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    version = Column(String(50), nullable=False)
    file_url = Column(String(500), nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    report = relationship("Report", back_populates="versions")
