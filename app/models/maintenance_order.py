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

    # العتاد
    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    # العملية المعرفة مسبقًا
    maintenance_type_id = Column(
        Integer,
        ForeignKey("maintenance_types.id"),
        nullable=False
    )

    # قراءة العداد وقت تنفيذ الصيانة
    meter_reading_id = Column(
        Integer,
        ForeignKey("meter_readings.id"),
        nullable=True
    )

    # وصف إضافي
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

    # الحالة
    status = Column(
        String(50),
        default="جارية",
        nullable=False
    )

    # ملاحظات
    notes = Column(
        String(500)
    )

    # العلاقات
    equipment = relationship(
        "Equipment",
        back_populates="maintenance_orders"
    )

    maintenance_type = relationship(
        "MaintenanceType"
    )

    meter_reading = relationship(
        "MeterReading"
    )
