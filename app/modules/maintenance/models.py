from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database.base import Base


# =========================================================
# Maintenance Type
# =========================================================

class MaintenanceType(Base):

    __tablename__ = "maintenance_types"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(100),
        nullable=False,
        unique=True
    )

    description = Column(
        String(300)
    )


# =========================================================
# Maintenance Schedule
# =========================================================

class MaintenanceSchedule(Base):

    __tablename__ = "maintenance_schedules"

    id = Column(
        Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # العتاد
    # -----------------------------------------------------

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    # -----------------------------------------------------
    # اسم عملية الصيانة
    # -----------------------------------------------------

    name = Column(
        String(150),
        nullable=False
    )

    # -----------------------------------------------------
    # شرط الصيانة بالعداد
    # -----------------------------------------------------

    interval_km = Column(
        Integer
    )

    # -----------------------------------------------------
    # شرط الصيانة بالأيام
    # -----------------------------------------------------

    interval_days = Column(
        Integer
    )

    # -----------------------------------------------------
    # آخر تنفيذ
    # -----------------------------------------------------

    last_maintenance_date = Column(
        Date
    )

    last_maintenance_meter = Column(
        Integer
    )

    # -----------------------------------------------------
    # الاستحقاق القادم
    # -----------------------------------------------------

    next_due_date = Column(
        Date
    )

    next_due_meter = Column(
        Integer
    )

    # -----------------------------------------------------
    # وصف وشروط العملية
    # -----------------------------------------------------

    description = Column(
        String(500)
    )

    # -----------------------------------------------------
    # العلاقات
    # -----------------------------------------------------

    equipment = relationship(
        "Equipment",
        back_populates="maintenance_schedules"
    )

    maintenance_orders = relationship(
        "MaintenanceOrder",
        back_populates="maintenance_schedule"
    )


# =========================================================
# Maintenance Order
# =========================================================

class MaintenanceOrder(Base):

    __tablename__ = "maintenance_orders"

    id = Column(
        Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # العتاد
    # -----------------------------------------------------

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    # -----------------------------------------------------
    # خطة الصيانة
    # -----------------------------------------------------

    maintenance_schedule_id = Column(
        Integer,
        ForeignKey("maintenance_schedules.id"),
        nullable=True
    )

    # -----------------------------------------------------
    # نوع / اسم العملية
    # -----------------------------------------------------

    maintenance_type = Column(
        String(100),
        nullable=False
    )

    # -----------------------------------------------------
    # وصف العمل أو العطل
    # -----------------------------------------------------

    description = Column(
        String(500)
    )

    # -----------------------------------------------------
    # تاريخ بدء الصيانة
    # -----------------------------------------------------

    maintenance_date = Column(
        Date
    )

    # -----------------------------------------------------
    # تاريخ انتهاء الصيانة
    # -----------------------------------------------------

    completion_date = Column(
        Date
    )

    # -----------------------------------------------------
    # قراءة العداد عند تنفيذ الصيانة
    # -----------------------------------------------------

    meter_reading = Column(
        Integer
    )

    # -----------------------------------------------------
    # حالة الصيانة
    # -----------------------------------------------------

    status = Column(
        String(50),
        default="جارية",
        nullable=False
    )

    # -----------------------------------------------------
    # الملاحظات
    # -----------------------------------------------------

    notes = Column(
        String(500)
    )

    # -----------------------------------------------------
    # العلاقات
    # -----------------------------------------------------

    equipment = relationship(
        "Equipment",
        back_populates="maintenance_orders"
    )

    maintenance_schedule = relationship(
        "MaintenanceSchedule",
        back_populates="maintenance_orders"
    )


# =========================================================
# Meter Reading
# =========================================================

class MeterReading(Base):

    __tablename__ = "meter_readings"

    id = Column(
        Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # العتاد
    # -----------------------------------------------------

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    # -----------------------------------------------------
    # قراءة العداد بالكيلومتر
    # -----------------------------------------------------

    reading_value = Column(
        Integer,
        nullable=False
    )

    # -----------------------------------------------------
    # تاريخ تسجيل القراءة
    # -----------------------------------------------------

    reading_date = Column(
        Date,
        nullable=False
    )

    # -----------------------------------------------------
    # العلاقة مع العتاد
    # -----------------------------------------------------

    equipment = relationship(
        "Equipment",
        back_populates="meter_readings"
  )
