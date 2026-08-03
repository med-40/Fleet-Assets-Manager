from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database.base import Base


class MaintenanceOrder(Base):

    __tablename__ = "maintenance_orders"

    id = Column(
        Integer,
        primary_key=True
    )

    # السيارة / العتاد
    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    # نوع عملية الصيانة
    # مثال:
    # إصلاح عطل
    # صيانة دورية
    # فحص
    # تشخيص
    # استبدال قطعة
    maintenance_type = Column(
        String(100),
        nullable=False
    )

    # وصف العمل أو العطل
    description = Column(
        String(500)
    )

    # تاريخ بدء الصيانة
    maintenance_date = Column(
        Date
    )

    # تاريخ انتهاء الصيانة
    completion_date = Column(
        Date
    )

    # حالة الصيانة
    # جارية / منتهية / ملغاة
    status = Column(
        String(50),
        default="جارية",
        nullable=False
    )

    # الملاحظات
    notes = Column(
        String(500)
    )

    # العلاقة مع العتاد
    equipment = relationship(
        "Equipment",
        back_populates="maintenance_orders"
    )
