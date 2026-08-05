from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Role(Base):

    __tablename__ = "roles"

    # =====================================================
    # المعرف
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # اسم الدور
    # =====================================================

    name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    # =====================================================
    # الوصف
    # =====================================================

    description = Column(
        String(255)
    )

    # =====================================================
    # حالة الدور
    # =====================================================

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )
