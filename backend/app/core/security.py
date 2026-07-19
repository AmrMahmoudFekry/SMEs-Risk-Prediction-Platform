import base64
import hashlib
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt

from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def _prehash(password: str) -> bytes:
    """
    bcrypt نفسه بيتجاهل أي بايت بعد أول 72 بايت من الباسورد، وبعض إصدارات
    مكتبة bcrypt الحديثة بترفض أي باسورد أطول من كده برسالة خطأ صريحة بدل
    التجاهل الصامت. لتفادي المشكلتين مع دعم أي طول باسورد بأمان، بنعمل
    hashing أولي بـ SHA-256 (ناتج ثابت الطول) قبل تمريره لـ bcrypt — نفس
    المبدأ اللي كان مفروض يوفره passlib's bcrypt_sha256، لكن بتنفيذ مباشر
    بدون الاعتماد على مكتبة passlib المتوقفة عن التطوير والتي لا تتوافق
    بشكل موثوق مع إصدارات bcrypt الحديثة (>=4.1).
    """
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(_prehash(plain_password), hashed_password.encode("utf-8"))
    except ValueError:
        return False


def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(_prehash(password), bcrypt.gensalt())
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt