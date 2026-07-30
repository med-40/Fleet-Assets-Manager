from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.database.base import Base


class Department(Base):

    __tablename__ = "departments"

    id = Column(
        Integer,
        primary_key=True
    )

    branch_id = Column(
        Integer,
        ForeignKey("branches.id"),
        nullable=False
    )

    name = Column(
        String(150),
        nullable=False
    )

    branch = relationship(
        "Branch"
    )
