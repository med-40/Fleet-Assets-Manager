from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Part(Base):

    __tablename__ = "parts"

    id = Column(
        Integer,
        primary_key=True
    )

    part_type_id = Column(
        Integer,
        ForeignKey("part_types.id"),
        nullable=False
    )

    name = Column(
        String(150),
        nullable=False
    )

    reference_number = Column(
        String(100)
    )

    manufacturer = Column(
        String(100)
    )

    unit = Column(
        String(50),
        default="Piece"
    )

    minimum_stock = Column(
        Integer,
        default=0
    )
