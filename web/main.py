from fastapi import FastAPI

from app.core.config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
)

from app.modules.maintenance.routes import router as maintenance_router


# =========================================================
# إنشاء التطبيق
# =========================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
)


# =========================================================
# Routers
# =========================================================

app.include_router(
    maintenance_router
)


# =========================================================
# الصفحة الرئيسية
# =========================================================

@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
    }


# =========================================================
# فحص النظام
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
    }
