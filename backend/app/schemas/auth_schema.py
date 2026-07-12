from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(..., description="User full name")
    email: EmailStr
    password: str = Field(..., min_length=8)
    organization_id: int
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
