from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class FuelLog(Base):

    __tablename__ = "fuel_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    date = Column(
        Date,
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    mileage = Column(
        Integer
    )

    fuel_type = Column(
        String(50)
    )

    notes = Column(
        String(300)
    )
