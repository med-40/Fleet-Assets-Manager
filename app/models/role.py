from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Role(Base):

    __tablename__ = "roles"

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
