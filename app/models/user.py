from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class User(Base):

    __tablename__ = "users"

    # =====================================================
    # المعرف
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # اسم المستخدم
    # =====================================================

    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    # =====================================================
    # كلمة المرور المشفرة
    # =====================================================

    password_hash = Column(
        String(255),
        nullable=False
    )

    # =====================================================
    # اسم المستخدم الظاهر
    # =====================================================

    full_name = Column(
        String(150),
        nullable=False
    )

    # =====================================================
    # الدور
    # =====================================================

    role = Column(
        String(50),
        nullable=False,
        default="viewer"
    )

    # =====================================================
    # حالة الحساب
    # =====================================================

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    # =====================================================
    # تاريخ إنشاء الحساب
    # =====================================================

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # =====================================================
    # آخر دخول
    # =====================================================

    last_login = Column(
        DateTime,
        nullable=True
    )
