from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class EquipmentStatus(Base):

    __tablename__ = "equipment_statuses"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(100),
        nullable=False,
        unique=True
    )

    description = Column(
        String(300)
    )
