import re
import secrets
from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, get_password_hash
from app.repositories.user_repository import UserRepository
from app.repositories.organization_repository import OrganizationRepository
from app.db.models import Organization
from app.schemas.auth_schema import (
    TokenResponse,
    UserCreate,
    OrganizationRegisterRequest,
    OrganizationRegisterResponse,
)
from app.core.config import settings


def _generate_tenant_code(organization_name: str) -> str:
    """
    يولّد كود مؤسسة (tenant_code) مقروء بشريًا من اسم المؤسسة، مع لاحقة
    عشوائية قصيرة لضمان التفرد، بدل الاعتماد على المعرف الرقمي التسلسلي
    (auto-increment id) الذي لا يجب كشفه للمستخدمين كمعرّف قابل للمشاركة.
    """
    slug = re.sub(r"[^A-Za-z0-9]+", "-", organization_name.strip()).strip("-").upper()
    suffix = secrets.token_hex(2).upper()
    return f"{slug[:40]}-{suffix}"


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.org_repo = OrganizationRepository(db)

    def authenticate(self, username: str, password: str) -> TokenResponse:
        user = self.user_repo.get_by_email(username)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        role_name = user.role.name if user.role else "User"
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "role": role_name},
            expires_delta=access_token_expires,
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            role=role_name,
        )

    def register_organization(self, data: OrganizationRegisterRequest) -> OrganizationRegisterResponse:
        """
        يُنشئ مؤسسة جديدة (بنك/شركة تمويل) مع أول مستخدم Admin لها في
        عملية واحدة. هذا هو المسار الوحيد الشرعي لإنشاء مستخدم بصلاحية
        Admin، بخلاف /register العادي المخصص للانضمام لمؤسسة قائمة والذي
        يمنع صراحةً اختيار دور Admin.
        """
        if self.user_repo.get_by_email(data.admin_email):
            raise ValueError("Email already registered")

        if self.org_repo.get_by_name(data.organization_name):
            raise ValueError("An organization with this name is already registered")

        tenant_code = _generate_tenant_code(data.organization_name)
        while self.org_repo.get_by_tenant_code(tenant_code):
            tenant_code = _generate_tenant_code(data.organization_name)

        organization = self.org_repo.create(
            Organization(
                name=data.organization_name,
                tenant_code=tenant_code,
                status="active",
            )
        )

        admin_role = self.user_repo.get_role_by_name("Admin")
        if not admin_role:
            raise ValueError("Admin role is not configured on this server. Please contact support.")

        hashed_password = get_password_hash(data.admin_password)
        user = self.user_repo.create_user(
            name=data.admin_name,
            email=data.admin_email,
            hashed_password=hashed_password,
            organization_id=organization.id,
            role_id=admin_role.id,
        )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "role": admin_role.name},
            expires_delta=access_token_expires,
        )

        return OrganizationRegisterResponse(
            access_token=access_token,
            token_type="bearer",
            role=admin_role.name,
            organization_id=organization.id,
            organization_name=organization.name,
            tenant_code=organization.tenant_code,
        )

    def register(self, user_data: UserCreate) -> TokenResponse:
        """تسجيل مستخدم جديد للانضمام إلى مؤسسة قائمة بالفعل عبر tenant_code."""
        if self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email already registered")

        if user_data.role_name.lower() == "admin":
            raise ValueError("Admin registration is restricted. Use the organization onboarding flow instead.")

        organization = self.org_repo.get_by_tenant_code(user_data.tenant_code)
        if not organization:
            raise ValueError("Invalid organization code. Please check with your institution admin.")

        role = self.user_repo.get_role_by_name(user_data.role_name)
        if not role:
            raise ValueError("Invalid role. Please choose a valid role.")

        hashed_password = get_password_hash(user_data.password)
        user = self.user_repo.create_user(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            organization_id=organization.id,
            role_id=role.id,
        )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "role": role.name},
            expires_delta=access_token_expires,
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            role=role.name,
        )