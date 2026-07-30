from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from app.database.base import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    message = Column(
        String(500)
    )

    notification_type = Column(
        String(100)
    )

    is_read = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )
