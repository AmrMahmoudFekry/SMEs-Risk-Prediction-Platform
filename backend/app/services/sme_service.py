from sqlalchemy.orm import Session

from app.repositories.sme_repository import SMERepository
from app.db.models import SME
from app.core.exceptions import SMENotFoundError, SMEAccessDeniedError
from app.schemas.sme_schema import SMECreate, SMEUpdate


class SMEService:
    def __init__(self, db: Session):
        self.db = db
        self.sme_repo = SMERepository(db)

    def _get_owned_sme(self, sme_id: int, organization_id: int) -> SME:
        """
        تحقق من عزل البيانات بين المستأجرين (tenant isolation) — نفس منطق
        الحماية المطبّق في assessment_service.py، لمنع أي مستخدم من
        الوصول لمنشأة تابعة لمؤسسة أخرى (IDOR protection).
        """
        sme = self.sme_repo.get_by_id(sme_id)
        if not sme:
            raise SMENotFoundError(f"SME with id {sme_id} was not found.")
        if sme.organization_id != organization_id:
            raise SMEAccessDeniedError("The requested SME does not belong to your organization.")
        return sme

    def create_sme(self, data: SMECreate, organization_id: int) -> SME:
        sme = SME(
            organization_id=organization_id,
            legal_name=data.legal_name,
            industry=data.industry,
            business_age_months=data.business_age_months,
            ownership_type=data.ownership_type,
            registration_date=data.registration_date,
            status="active",
        )
        return self.sme_repo.create(sme)

    def get_sme(self, sme_id: int, organization_id: int) -> SME:
        return self._get_owned_sme(sme_id, organization_id)

    def list_smes(
        self,
        organization_id: int,
        skip: int,
        limit: int,
        search: str | None,
        industry: str | None,
    ):
        items = self.sme_repo.list_by_organization(organization_id, skip, limit, search, industry)
        total = self.sme_repo.count_by_organization(organization_id, search, industry)
        return items, total

    def update_sme(self, sme_id: int, organization_id: int, data: SMEUpdate) -> SME:
        sme = self._get_owned_sme(sme_id, organization_id)
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(sme, field, value)
        return self.sme_repo.update(sme)

    def delete_sme(self, sme_id: int, organization_id: int) -> None:
        sme = self._get_owned_sme(sme_id, organization_id)
        self.sme_repo.delete(sme)

    def get_sme_with_latest_assessment(self, sme_id: int, organization_id: int):
        sme = self._get_owned_sme(sme_id, organization_id)
        latest = self.sme_repo.get_latest_assessment(sme_id)
        return sme, latest