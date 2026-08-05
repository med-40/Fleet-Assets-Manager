from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Permission(Base):

    __tablename__ = "permissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False,
        index=True
    )

    module = Column(
        String(100),
        nullable=False,
        index=True
    )

    can_view = Column(
        Boolean,
        nullable=False,
        default=False
    )

    can_create = Column(
        Boolean,
        nullable=False,
        default=False
    )

    can_edit = Column(
        Boolean,
        nullable=False,
        default=False
    )

    can_delete = Column(
        Boolean,
        nullable=False,
        default=False
    )

    role = relationship(
        "Role",
        back_populates="permissions"
    )
