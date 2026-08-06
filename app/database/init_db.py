from app.database.base import Base
from app.database.session import engine


# =========================================================
# استيراد Models
# =========================================================

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.notification import Notification

from app.models.equipment import Equipment

from app.modules.maintenance.models import (
    MaintenanceOrder,
    MaintenanceSchedule,
    MaintenanceType,
    MeterReading,
)


# =========================================================
# تهيئة قاعدة البيانات
# =========================================================

def init_database():
    """
    إنشاء الجداول المسجلة في Base.
    """

    Base.metadata.create_all(
        bind=engine
    )


# =========================================================
# تشغيل مباشر
# =========================================================

if __name__ == "__main__":
    init_database()
