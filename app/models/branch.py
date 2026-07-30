from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.database.base import Base


class Branch(Base):

    __tablename__ = "branches"

    id = Column(
        Integer,
        primary_key=True
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False
    )

    name = Column(
        String(150),
        nullable=False
    )

    organization = relationship(
        "Organization"
    )
