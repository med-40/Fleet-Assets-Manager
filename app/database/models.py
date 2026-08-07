# =========================================================
# تسجيل نماذج قاعدة البيانات
# =========================================================

from app.models.equipment import Equipment

from app.modules.maintenance.models import (
    MaintenanceType,
    MaintenanceSchedule,
    MaintenanceOrder,
    MeterReading,
)
