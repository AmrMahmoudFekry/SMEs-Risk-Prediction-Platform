from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token, get_password_hash
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import TokenResponse, UserCreate
from app.core.config import settings

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

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

    def register(self, user_data: UserCreate) -> TokenResponse:
        if self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email already registered")

        if user_data.role_name.lower() == "admin":
            raise ValueError("Admin registration is restricted")

        role = self.user_repo.get_role_by_name(user_data.role_name)
        if not role:
            raise ValueError("Invalid role. Please choose a valid role.")

        hashed_password = get_password_hash(user_data.password)
        user = self.user_repo.create_user(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            organization_id=user_data.organization_id,
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
