from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.database.base import Base


class WorkshopTransfer(Base):

    __tablename__ = "workshop_transfers"

    id = Column(
        Integer,
        primary_key=True
    )

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    # اسم الورشة الخارجية
    workshop_name = Column(
        String(200),
        nullable=False
    )

    # وثيقة إرسال العتاد إلى الورشة
    dispatch_document = Column(
        String(100),
        nullable=False
    )

    # تاريخ الإرسال
    dispatch_date = Column(
        Date,
        nullable=False
    )

    # تاريخ العودة المتوقع
    expected_return_date = Column(
        Date
    )

    # تاريخ العودة الفعلي
    actual_return_date = Column(
        Date
    )

    # سبب إرسال العتاد
    reason = Column(
        String(500)
    )

    # الحالة
    status = Column(
        String(50),
        default="في الورشة",
        nullable=False
    )

    # الملاحظات
    notes = Column(
        String(500)
    )

    equipment = relationship(
        "Equipment",
        back_populates="workshop_transfers"
    )
