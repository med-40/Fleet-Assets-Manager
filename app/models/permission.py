from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Permission(Base):

    __tablename__ = "permissions"

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
