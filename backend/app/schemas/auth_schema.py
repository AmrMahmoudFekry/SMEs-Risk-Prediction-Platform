from pydantic import BaseModel, EmailStr, Field


class OrganizationRegisterRequest(BaseModel):
    """طلب تسجيل مؤسسة جديدة (بنك/شركة تمويل) مع أول مستخدم Admin لها."""
    organization_name: str = Field(..., min_length=2, max_length=255, description="Legal name of the institution")
    admin_name: str = Field(..., min_length=2, description="Full name of the first administrator")
    admin_email: EmailStr
    admin_password: str = Field(..., min_length=8)


class OrganizationRegisterResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    organization_id: int
    organization_name: str
    tenant_code: str


class UserCreate(BaseModel):
    """تسجيل مستخدم جديد للانضمام إلى مؤسسة قائمة بالفعل عبر كود المؤسسة."""
    name: str = Field(..., description="User full name")
    email: EmailStr
    password: str = Field(..., min_length=8)
    tenant_code: str = Field(..., description="Organization tenant code provided by your institution admin")
    role_name: str = Field(default="Analyst", description="Role name assigned to the user")


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    organization_id: int
    role: str

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str