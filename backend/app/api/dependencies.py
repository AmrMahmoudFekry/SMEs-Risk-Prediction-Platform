
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.core.security import SECRET_KEY, ALGORITHM

# تحديد مسار تسجيل الدخول الذي سيتم استخدامه لاستخراج التوكن
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # فك تشفير التوكن
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # التحقق من وجود المستخدم في قاعدة البيانات
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_admin(current_user: User = Depends(get_current_user)):
    """صلاحية مخصصة لمديري النظام (Admins) فقط"""
    if current_user.role is None or current_user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user