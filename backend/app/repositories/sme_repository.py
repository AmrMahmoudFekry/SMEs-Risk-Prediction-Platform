from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from app.db.models import SME, Assessment


class SMERepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, sme: SME) -> SME:
        self.db.add(sme)
        self.db.commit()
        self.db.refresh(sme)
        return sme

    def get_by_id(self, sme_id: int) -> Optional[SME]:
        return self.db.query(SME).filter(SME.id == sme_id).first()

    def list_by_organization(
        self,
        organization_id: int,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        industry: Optional[str] = None,
    ) -> List[SME]:
        query = self.db.query(SME).filter(SME.organization_id == organization_id)
        if search:
            query = query.filter(SME.legal_name.ilike(f"%{search}%"))
        if industry:
            query = query.filter(SME.industry == industry)
        return query.order_by(SME.created_at.desc()).offset(skip).limit(limit).all()

    def count_by_organization(
        self,
        organization_id: int,
        search: Optional[str] = None,
        industry: Optional[str] = None,
    ) -> int:
        query = self.db.query(func.count(SME.id)).filter(SME.organization_id == organization_id)
        if search:
            query = query.filter(SME.legal_name.ilike(f"%{search}%"))
        if industry:
            query = query.filter(SME.industry == industry)
        return query.scalar()

    def update(self, sme: SME) -> SME:
        self.db.commit()
        self.db.refresh(sme)
        return sme

    def delete(self, sme: SME) -> None:
        self.db.delete(sme)
        self.db.commit()

    def get_latest_assessment(self, sme_id: int) -> Optional[Assessment]:
        return (
            self.db.query(Assessment)
            .filter(Assessment.sme_id == sme_id)
            .order_by(Assessment.created_at.desc())
            .first()
        )