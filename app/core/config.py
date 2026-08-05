from pathlib import Path


# =========================================================
# المسارات الأساسية للمشروع
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

APP_DIR = PROJECT_ROOT / "app"

WEB_DIR = PROJECT_ROOT / "web"

TEMPLATES_DIR = PROJECT_ROOT / "templates"

STATIC_DIR = PROJECT_ROOT / "static"

DATABASE_DIR = PROJECT_ROOT / "data"

DATABASE_FILE = DATABASE_DIR / "fleet_assets.db"


# =========================================================
# إعدادات التطبيق
# =========================================================

APP_NAME = "Fleet Assets Manager"

APP_VERSION = "1.0.0"

APP_DESCRIPTION = "نظام تسيير وإدارة الحضيرة"


# =========================================================
# إعدادات قاعدة البيانات
# =========================================================

DATABASE_URL = (
    f"sqlite:///{DATABASE_FILE}"
)


# =========================================================
# إعدادات الجلسة
# =========================================================

SESSION_COOKIE_NAME = "fleet_session"

SESSION_EXPIRE_MINUTES = 60


# =========================================================
# إعدادات الأمان
# =========================================================

SECRET_KEY = "CHANGE_THIS_SECRET_KEY"

ALGORITHM = "HS256"


# =========================================================
# إعدادات اللغة
# =========================================================

DEFAULT_LANGUAGE = "ar"

DEFAULT_DIRECTION = "rtl"
