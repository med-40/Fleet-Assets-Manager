from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Driver(Base):

    __tablename__ = "drivers"

    id = Column(
        Integer,
        primary_key=True
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    # الرتبة
    rank = Column(
        String(100)
    )

    # الهاتف
    phone = Column(
        String(50)
    )

    # رخصة السياقة
    license_number = Column(
        String(100),
        unique=True
    )

    license_expiry_date = Column(
        Date
    )

    # الحالة الإدارية للسائق
    status = Column(
        String(50),
        default="Active"
    )

    # -----------------------------------------------------
    # التأهيل
    # -----------------------------------------------------

    # هل اجتاز السائق مرحلة التأكيد؟
    qualification_confirmed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    # درجة التأهيل:
    # سيئ / حسن / جيد
    #
    # إذا qualification_confirmed = False
    # يعتبر السائق غير مؤهل مهما كانت قيمة هذا الحقل.
    qualification_level = Column(
        String(20),
        nullable=True
    )
