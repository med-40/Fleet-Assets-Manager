from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from app.database.base import Base


class Stock(Base):

    __tablename__ = "stocks"

    id = Column(
        Integer,
        primary_key=True
    )

    part_id = Column(
        Integer,
        ForeignKey("parts.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        default=0
    )
