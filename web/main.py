from datetime import date
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from app.database.session import SessionLocal
from app.models.equipment import Equipment
from app.models.equipment_type import EquipmentType
from app.models.driver import Driver


# =========================================================
# إعدادات التطبيق
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
INDEX_FILE = TEMPLATES_DIR / "index.html"

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


app = FastAPI(
    title="Fleet Assets Manager",
    description="نظام تسيير الحضيرة",
    version="1.0.0"
)


# =========================================================
# الصفحة الرئيسية
# =========================================================

@app.get("/")
def home():

    return FileResponse(INDEX_FILE)


# =========================================================
# Dashboard
# =========================================================

@app.get("/dashboard")
def dashboard(request: Request):

    db = SessionLocal()

    try:

        vehicles = 0
        active_missions = 0
        due_maintenance = 0
        monthly_fuel = 0
        batteries = 0
        tires = 0

        try:
            vehicles = db.execute(
                text("SELECT COUNT(*) FROM equipment")
            ).scalar() or 0
        except Exception:
            vehicles = 0

        try:
            active_missions = db.execute(
                text("""
                    SELECT COUNT(*)
                    FROM missions
                    WHERE status = 'جارية'
                """)
            ).scalar() or 0
        except Exception:
            active_missions = 0

        try:
            due_maintenance = db.execute(
                text("""
                    SELECT COUNT(*)
                    FROM maintenance_orders
                """)
            ).scalar() or 0
        except Exception:
            due_maintenance = 0

        try:
            monthly_fuel = db.execute(
                text("""
                    SELECT COALESCE(SUM(quantity), 0)
                    FROM fuel_logs
                """)
            ).scalar() or 0
        except Exception:
            monthly_fuel = 0

        try:
            batteries = db.execute(
                text("""
                    SELECT COUNT(*)
                    FROM batteries
                """)
            ).scalar() or 0
        except Exception:
            batteries = 0

        try:
            tires = db.execute(
                text("""
                    SELECT COUNT(*)
                    FROM tires
                """)
            ).scalar() or 0
        except Exception:
            tires = 0

        return templates.TemplateResponse(
            request=request,
            name
