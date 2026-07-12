from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(String(1000), nullable=True)
    notification_type = Column(String(100), nullable=False)
    is_read = Column(Boolean, default=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")
    organization = relationship("Organization", back_populates="notifications")
