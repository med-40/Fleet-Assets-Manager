from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class PartRequest(Base):

    __tablename__ = "part_requests"

    id = Column(
        Integer,
        primary_key=True
    )

    part_id = Column(
        Integer,
        ForeignKey("parts.id"),
        nullable=False
    )

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id")
    )

    quantity = Column(
        Integer,
        default=1
    )

    request_date = Column(
        Date
    )

    status = Column(
        String(50),
        default="Open"
    )

    notes = Column(
        String(500)
    )
