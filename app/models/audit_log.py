from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from app.database.base import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    action = Column(
        String(50),
        nullable=False
    )

    table_name = Column(
        String(100),
        nullable=False
    )

    record_id = Column(
        Integer
    )

    old_value = Column(
        String(1000)
    )

    new_value = Column(
        String(1000)
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )
