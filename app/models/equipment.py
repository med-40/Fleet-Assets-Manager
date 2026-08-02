from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy.orm import relationship

from app.database.base import Base


class Equipment(Base):

    __tablename__ = "equipment"

    id = Column(
        Integer,
        primary_key=True
    )

    # وثيقة الاستلام
    receipt_document = Column(
        String(100),
        unique=True,
        nullable=False
    )

    # نوع العتاد
    equipment_type_id = Column(
        Integer,
        ForeignKey("equipment_types.id"),
        nullable=False
    )

    # الطراز
    model = Column(
        String(100)
    )

    # رقم التسجيل
    registration_number = Column(
        String(100),
        unique=True,
        nullable=False
    )

    # رقم الهيكل
    chassis_number = Column(
        String(150),
        unique=True
    )

    # الحالة
    status = Column(
        String(50),
        default="متاحة"
    )

    # المصلحة
    department = Column(
        String(150)
    )

    # نوع الوقود
    fuel_type = Column(
        String(50)
    )

    # معدل الاستهلاك
    fuel_consumption = Column(
        Float
    )

    # الملاحظات
    notes = Column(
        String(500)
    )

    # العلاقة مع نوع العتاد
    equipment_type = relationship(
        "EquipmentType"
    )

    # العلاقة مع التحويلات إلى الورش الخارجية
    workshop_transfers = relationship(
        "WorkshopTransfer",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )
