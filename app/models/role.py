from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Role(Base):

    __tablename__ = "roles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    description = Column(
        String(255)
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    users = relationship(
        "User",
        back_populates="role"
    )

    permissions = relationship(
        "Permission",
        back_populates="role",
        cascade="all, delete-orphan"
    )
