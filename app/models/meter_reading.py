from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import relationship

from app.database.base import Base


class MeterReading(Base):

    __tablename__ = "meter_readings"

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

    # قراءة العداد بالكيلومتر
    reading_value = Column(
        Integer,
        nullable=False
    )

    # تاريخ تسجيل القراءة
    reading_date = Column(
        Date,
        nullable=False
    )

    # العلاقة مع العتاد
    equipment = relationship(
        "Equipment",
        back_populates="meter_readings"
    )
