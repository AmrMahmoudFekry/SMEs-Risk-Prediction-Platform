from sqlalchemy.orm import Session
from app.db.models import User, Role

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_role_by_name(self, role_name: str) -> Role | None:
        return self.db.query(Role).filter(Role.name == role_name).first()

    def get_role_by_id(self, role_id: int) -> Role | None:
        return self.db.query(Role).filter(Role.id == role_id).first()

    def list_all(self) -> list[User]:
        return self.db.query(User).order_by(User.id.desc()).all()

    def list_roles(self) -> list[Role]:
        return self.db.query(Role).order_by(Role.name).all()

    def create_user(
        self,
        name: str,
        email: str,
        hashed_password: str,
        organization_id: int,
        role_id: int,
        phone: str | None = None,
    ) -> User:
        user = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            organization_id=organization_id,
            role_id=role_id,
            phone=phone,
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
