from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
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

    registration_number = Column(
        String(100),
        unique=True
    )

    manufacturer = Column(
        String(100)
    )

    model = Column(
        String(100)
    )

    year = Column(
        Integer
    )

    chassis_number = Column(
        String(150)
    )

    engine_number = Column(
        String(150)
    )

    acquisition_date = Column(
        Date
    )

    status = Column(
        String(50),
        default="Active"
    )

    equipment_type = relationship(
        "EquipmentType"
    )
