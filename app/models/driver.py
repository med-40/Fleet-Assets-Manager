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

    # الاسم
    first_name = Column(
        String(100),
        nullable=False
    )

    # اللقب
    last_name = Column(
        String(100),
        nullable=False
    )

    # الرتبة
    rank = Column(
        String(100),
        nullable=True
    )

    # الهاتف
    phone = Column(
        String(50),
        nullable=True
    )

    # رقم رخصة السياقة
    license_number = Column(
        String(100),
        unique=True,
        nullable=True
    )

    # تاريخ انتهاء رخصة السياقة
    license_expiry_date = Column(
        Date,
        nullable=True
    )

    # الحالة الإدارية للسائق
    status = Column(
        String(50),
        default="Active",
        nullable=False
    )

    # =====================================================
    # التأهيل
    # =====================================================

    # هل اجتاز السائق مرحلة التأكيد؟
    #
    # False = غير مؤهل
    # True  = أصبح مؤهلاً ويمكن تحديد مستوى التأهيل
    qualification_confirmed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    # مستوى التأهيل:
    #
    # سيئ
    # حسن
    # جيد
    #
    # إذا كانت qualification_confirmed = False
    # فإن السائق يعتبر غير مؤهل مهما كانت قيمة هذا الحقل.
    qualification_level = Column(
        String(20),
        nullable=True
    )
