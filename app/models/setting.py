from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class Setting(Base):

    __tablename__ = "settings"

    id = Column(
        Integer,
        primary_key=True
    )

    key = Column(
        String(100),
        nullable=False,
        unique=True
    )

    value = Column(
        String(500)
    )

    description = Column(
        String(300)
    )
