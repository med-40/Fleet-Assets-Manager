from app.database.base import Base
from app.database.session import engine

# =========================================================
# استيراد Models
# =========================================================

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission


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
