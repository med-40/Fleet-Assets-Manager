from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.orm import relationship

from app.database.base import Base


class MaintenanceOrder(Base):

    __tablename__ = "maintenance_orders"

    id = Column(
        Integer,
        primary_key=True
    )

    # السيارة
    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    # نوع الورشة
    workshop_type = Column(
        String(50),
        nullable=False,
        default="داخل المؤسسة"
    )

    # اسم الورشة الخارجية
    workshop_name = Column(
        String(200)
    )

    # سبب إرسال السيارة
    reason = Column(
        String(500)
    )

    # وثيقة إرسال السيارة إلى الورشة
    dispatch_document = Column(
        String(100)
    )

    # تاريخ إرسال السيارة
    dispatch_date = Column(
        Date
    )

    # وثيقة إرجاع السيارة
    return_document = Column(
        String(100)
    )

    # تاريخ إرجاع السيارة
    return_date = Column(
        Date
    )

    # حالة العملية
    status = Column(
        String(50),
        default="خارج المؤسسة"
    )

    # ملاحظات
    notes = Column(
        String(500)
    )

    # العلاقة مع السيارة
    equipment = relationship(
        "Equipment"
    )
