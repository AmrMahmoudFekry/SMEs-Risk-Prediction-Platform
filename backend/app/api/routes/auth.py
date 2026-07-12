from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth_schema import TokenResponse, UserCreate, UserOut
from app.api.dependencies import get_current_user, get_current_active_admin
from app.db.models import User

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    try:
        return auth_service.authenticate(form_data.username, form_data.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", response_model=TokenResponse)
async def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    try:
        return auth_service.register(user_create)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/me", response_model=UserOut)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return UserOut(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        organization_id=current_user.organization_id,
        role=current_user.role.name if current_user.role else "User",
    )

@router.get("/users", response_model=List[UserOut])
async def list_users(current_user: User = Depends(get_current_active_admin), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user_repo = auth_service.user_repo
    users = user_repo.list_all()
    return [
        UserOut(
            id=user.id,
            name=user.name,
            email=user.email,
            organization_id=user.organization_id,
            role=user.role.name if user.role else "User",
        )
        for user in users
    ]
