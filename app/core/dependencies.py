from fastapi import Cookie, HTTPException, status

from app.core.config import SESSION_COOKIE_NAME
from app.core.security import decode_access_token


# =========================================================
# المستخدم الحالي من جلسة الدخول
# =========================================================

def get_current_user(
    session_token: str | None = Cookie(
        default=None,
        alias=SESSION_COOKIE_NAME,
    ),
):
    """
    الحصول على بيانات المستخدم من Cookie الجلسة.
    """

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="يجب تسجيل الدخول أولًا.",
        )

    payload = decode_access_token(
        session_token
    )

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="جلسة الدخول غير صالحة أو منتهية.",
        )

    user_id = payload.get("sub")
    username = payload.get("username")

    if not user_id or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="بيانات جلسة الدخول غير صحيحة.",
        )

    return {
        "id": int(user_id),
        "username": username,
    }


# =========================================================
# التحقق من صلاحية المستخدم
# =========================================================

def require_permission(
    module: str,
    action: str,
):
    """
    إنشاء Dependency للتحقق من صلاحية معينة.

    ملاحظة:
    في هذه المرحلة نتحقق من الجلسة فقط.
    بعد إنشاء User Model سنربط الدور والصلاحيات
    بقاعدة البيانات.
    """

    def permission_checker(
        current_user= get_current_user,
    ):
        return current_user

    return permission_checker
