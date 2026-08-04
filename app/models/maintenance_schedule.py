from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database.base import Base


class MaintenanceSchedule(Base):

    __tablename__ = "maintenance_schedules"

    id = Column(
        Integer,
        primary_key=True
    )

    # =====================================================
    # العتاد
    # =====================================================

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    # =====================================================
    # اسم عملية الصيانة
    # =====================================================

    name = Column(
        String(150),
        nullable=False
    )

    # =====================================================
    # شرط الصيانة بالعداد
    # =====================================================

    interval_km = Column(
        Integer
    )

    # =====================================================
    # شرط الصيانة بالأيام
    # =====================================================

    interval_days = Column(
        Integer
    )

    # =====================================================
    # آخر تنفيذ
    # =====================================================

    last_maintenance_date = Column(
        Date
    )

    last_maintenance_meter = Column(
        Integer
    )

    # =====================================================
    # الاستحقاق القادم
    # =====================================================

    next_due_date = Column(
        Date
    )

    next_due_meter = Column(
        Integer
    )

    # =====================================================
    # وصف وشروط العملية
    # =====================================================

    description = Column(
        String(500)
    )

    # =====================================================
    # العلاقات
    # =====================================================

    equipment = relationship(
        "Equipment",
        back_populates="maintenance_schedules"
    )

    maintenance_orders = relationship(
        "MaintenanceOrder",
        back_populates="maintenance_schedule"
    )
