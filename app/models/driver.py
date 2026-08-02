from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Driver(Base):

    __tablename__ = "drivers"

    # المعرف
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
        String(100)
    )

    # الهاتف
    phone = Column(
        String(50)
    )

    # رقم رخصة السياقة
    license_number = Column(
        String(100),
        unique=True
    )

    # تاريخ انتهاء رخصة السياقة
    license_expiry_date = Column(
        Date
    )

    # الحالة
    status = Column(
        String(50),
        default="Active"
    )
