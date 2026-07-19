from sqlalchemy.orm import Session
from app.db.models import Organization


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_tenant_code(self, tenant_code: str) -> Organization | None:
        return self.db.query(Organization).filter(Organization.tenant_code == tenant_code).first()

    def get_by_name(self, name: str) -> Organization | None:
        return self.db.query(Organization).filter(Organization.name == name).first()

    def get_by_id(self, organization_id: int) -> Organization | None:
        return self.db.query(Organization).filter(Organization.id == organization_id).first()

    def create(self, organization: Organization) -> Organization:
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)
        return organization