# تحميل جميع النماذج التي تعتمد عليها قاعدة البيانات
# حتى تقوم SQLAlchemy بتسجيل العلاقات بشكل صحيح.

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

from app.models.equipment import Equipment

from app.modules.maintenance.models import (
    MaintenanceOrder,
    MaintenanceSchedule,
    MaintenanceType,
    MeterReading,
)

__all__ = [
    "User",
    "Role",
    "Permission",
    "Equipment",
    "MaintenanceOrder",
    "MaintenanceSchedule",
    "MaintenanceType",
    "MeterReading",
]
