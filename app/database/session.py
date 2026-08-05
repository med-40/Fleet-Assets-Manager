from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL, DATABASE_DIR


# =========================================================
# إنشاء مجلد قاعدة البيانات
# =========================================================

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# محرك قاعدة البيانات
# =========================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
)


# =========================================================
# جلسات قاعدة البيانات
# =========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# =========================================================
# الحصول على جلسة قاعدة البيانات
# =========================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
