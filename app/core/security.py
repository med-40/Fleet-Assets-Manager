from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    SESSION_EXPIRE_MINUTES,
)


# =========================================================
# تشفير كلمات المرور
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    تحويل كلمة المرور إلى قيمة مشفرة
    قبل تخزينها في قاعدة البيانات.
    """

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    التحقق من كلمة المرور المدخلة
    مقابل كلمة المرور المشفرة.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# =========================================================
# إنشاء رمز تسجيل الدخول
# =========================================================

def create_access_token(
    user_id: int,
    username: str,
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=SESSION_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# =========================================================
# قراءة رمز تسجيل الدخول
# =========================================================

def decode_access_token(
    token: str,
):
    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload

    except JWTError:

        return None
