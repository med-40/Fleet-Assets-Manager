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

    # تاريخ انتهاء رخصة السياقة
    license_expiry_date = Column(
        Date
    )

    # الحالة العامة للسائق
    status = Column(
        String(50),
        default="Active"
    )

    # =====================================================
    # التأهيل
    # =====================================================

    # هل اجتاز السائق مرحلة التأكيد؟
    # False = لم يجتزها وبالتالي غير مؤهل
    # True  = اجتازها ويمكن أن تكون له درجة تأهيل
    qualification_confirmed = Column(
        Integer,
        default=0,
        nullable=False
    )

    # درجة التأهيل بعد اجتياز مرحلة التأكيد
    # القيم:
    # سيئ / حسن / جيد
    qualification_level = Column(
        String(50),
        nullable=True
    )
