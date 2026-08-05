from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Permission(Base):

    __tablename__ = "permissions"

    # =====================================================
    # المعرف
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # الدور
    # =====================================================

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False,
        index=True
    )

    # =====================================================
    # اسم الوحدة
    # =====================================================

    module = Column(
        String(100),
        nullable=False,
        index=True
    )

    # =====================================================
    # مشاهدة
    # =====================================================

    can_view = Column(
        Boolean,
        nullable=False,
        default=False
    )

    # =====================================================
    # إضافة
    # =====================================================

    can_create = Column(
        Boolean,
        nullable=False,
        default=False
    )

    # =====================================================
    # تعديل
    # =====================================================

    can_edit = Column(
        Boolean,
        nullable=False,
        default=False
    )

    # =====================================================
    # حذف
    # =====================================================

    can_delete = Column(
        Boolean,
        nullable=False,
        default=False
    )
