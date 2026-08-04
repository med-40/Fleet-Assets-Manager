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

    # =====================================================
    # العتاد
    # =====================================================

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    # =====================================================
    # خطة الصيانة التي تم تنفيذها
    # =====================================================
    #
    # لا نكتب اسم العملية يدويًا هنا.
    #
    # المستخدم يختار العملية من خطة الصيانة
    # الخاصة بالعتاد.
    #
    # مثال:
    # تغيير زيت المحرك
    # فحص الفرامل
    # تغيير فلتر الهواء
    #
    # =====================================================

    maintenance_schedule_id = Column(
        Integer,
        ForeignKey("maintenance_schedules.id"),
        nullable=True
    )

    # =====================================================
    # وصف إضافي
    # =====================================================

    description = Column(
        String(500)
    )

    # =====================================================
    # تاريخ بدء الصيانة
    # =====================================================

    maintenance_date = Column(
        Date
    )

    # =====================================================
    # تاريخ انتهاء الصيانة
    # =====================================================

    completion_date = Column(
        Date
    )

    # =====================================================
    # حالة الصيانة
    # =====================================================
    #
    # جارية
    # منتهية
    # ملغاة
    #
    # =====================================================

    status = Column(
        String(50),
        default="جارية",
        nullable=False
    )

    # =====================================================
    # الملاحظات
    # =====================================================

    notes = Column(
        String(500)
    )

    # =====================================================
    # قراءة العداد التي تمت عند تنفيذ الصيانة
    # =====================================================
    #
    # هذه القراءة مهمة جدًا.
    #
    # مثال:
    #
    # خطة تغيير الزيت كل 10,000 كم
    #
    # تم تنفيذها عند:
    # 125,000 كم
    #
    # النظام يستخدم هذه القراءة كأساس
    # لحساب الاستحقاق القادم.
    #
    # =====================================================

    meter_reading_id = Column(
        Integer,
        ForeignKey("meter_readings.id"),
        nullable=True
    )

    # =====================================================
    # العلاقات
    # =====================================================

    # العتاد
    equipment = relationship(
        "Equipment",
        back_populates="maintenance_orders"
    )

    # خطة الصيانة
    maintenance_schedule = relationship(
        "MaintenanceSchedule"
    )

    # قراءة العداد وقت تنفيذ الصيانة
    meter_reading = relationship(
        "MeterReading"
    )
