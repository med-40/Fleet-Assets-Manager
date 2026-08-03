from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Driver(Base):

    __tablename__ = "drivers"

    id = Column(
        Integer,
        primary_key=True
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    # الرتبة
    rank = Column(
        String(100)
    )

    phone = Column(
        String(50)
    )

    license_number = Column(
        String(100),
        unique=True
    )

    license_expiry_date = Column(
        Date
    )

    status = Column(
        String(50),
        default="Active"
    )
