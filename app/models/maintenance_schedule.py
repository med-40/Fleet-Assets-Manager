from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class MaintenanceSchedule(Base):

    __tablename__ = "maintenance_schedules"

    id = Column(
        Integer,
        primary_key=True
    )

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    )

    maintenance_type_id = Column(
        Integer,
        ForeignKey("maintenance_types.id"),
        nullable=False
    )

    interval_km = Column(
        Integer
    )

    interval_days = Column(
        Integer
    )

    last_maintenance_date = Column(
        Date
    )

    next_due_date = Column(
        Date
    )

    description = Column(
        String(300)
    )
