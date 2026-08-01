from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from sqlalchemy.orm import relationship

from app.database.base import Base


class Equipment(Base):

    __tablename__ = "equipment"

    id = Column(
        Integer,
        primary_key=True
    )

    equipment_type_id = Column(
        Integer,
        ForeignKey("equipment_types.id"),
        nullable=False
    )

    # وثيقة الاستلام
    receipt_document = Column(
        String(100),
        unique=True,
        nullable=False
    )

    # تاريخ الاقتناء
    acquisition_date = Column(
        Date
    )

    # رقم التسجيل
    registration_number = Column(
        String(100),
        unique=True,
        nullable=False
    )

    # العلامة
    manufacturer = Column(
        String(100)
    )

    # الطراز
    model = Column(
        String(100)
    )

    # رقم الهيكل
    chassis_number = Column(
        String(150),
        unique=True
    )

    # نوع الوقود
    fuel_type = Column(
        String(50)
    )

    # معدل الاستهلاك
    fuel_consumption = Column(
        Float
    )

    # الحالة
    status = Column(
        String(50),
        default="متاحة"
    )

    # تاريخ آخر مراجعة
    last_review_date = Column(
        Date
    )

    # المصلحة
    department = Column(
        String(150)
    )

    # الملاحظات
    notes = Column(
        String(500)
    )

    # نوع العتاد
    equipment_type = relationship(
        "EquipmentType"
    )

    # سجل إرسال العتاد إلى الورش الخارجية
    workshop_transfers = relationship(
        "WorkshopTransfer",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )
