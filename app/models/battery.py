from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Battery(Base):

    __tablename__ = "batteries"

    id = Column(
        Integer,
        primary_key=True
    )

    part_id = Column(
        Integer,
        ForeignKey("parts.id")
    )

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id")
    )

    serial_number = Column(
        String(100)
    )

    installation_date = Column(
        Date
    )

    replacement_date = Column(
        Date
    )

    installation_mileage = Column(
        Integer
    )

    replacement_mileage = Column(
        Integer
    )

    status = Column(
        String(50),
        default="Installed"
    )
