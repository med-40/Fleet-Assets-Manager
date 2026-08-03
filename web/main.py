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
# فحص الصحة (يستخدمه CI للتأكد أن السيرفر يعمل)
# =========================================================

@app.get("/health")
def health():
    return {"status": "ok"}


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
            name="pages/dashboard.html",
            context={
                "vehicles": vehicles,
                "active_missions": active_missions,
                "due_maintenance": due_maintenance,
                "monthly_fuel": monthly_fuel,
                "open_faults": 0,
                "batteries": batteries,
                "tires": tires,
                "expiring_licenses": 0,
            }
        )

    finally:
        db.close()


# =========================================================
# قائمة السيارات والعتاد
# =========================================================

@app.get("/equipment")
def equipment_page(request: Request):

    db = SessionLocal()

    try:
        equipment_list = (
            db.query(Equipment)
            .order_by(Equipment.registration_number)
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="pages/equipment.html",
            context={
                "equipment_list": equipment_list
            }
        )

    finally:
        db.close()


# =========================================================
# قائمة أنواع العتاد (JSON - يستخدمه CI)
# =========================================================

@app.get("/equipment-types")
def equipment_types_list():

    db = SessionLocal()

    try:
        equipment_types = (
            db.query(EquipmentType)
            .order_by(EquipmentType.name)
            .all()
        )

        return [
            {
                "id": equipment_type.id,
                "name": equipment_type.name
            }
            for equipment_type in equipment_types
        ]

    finally:
        db.close()


# =========================================================
# إضافة عتاد - صفحة النموذج
# =========================================================

@app.get("/equipment/new")
def new_equipment_page(request: Request):

    db = SessionLocal()

    try:
        equipment_types = (
            db.query(EquipmentType)
            .order_by(EquipmentType.name)
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="pages/equipment_form.html",
            context={
                "equipment_types": equipment_types,
                "error": None
            }
        )

    finally:
        db.close()


# =========================================================
# إضافة عتاد - حفظ البيانات
# =========================================================

@app.post("/equipment/new")
def create_equipment(
    request: Request,
    receipt_document: str = Form(...),
    equipment_type_id: int = Form(...),
    model: str = Form(""),
    registration_number: str = Form(...),
    chassis_number: str = Form(""),
    status: str = Form("متاحة"),
    department: str = Form(""),
    fuel_type: str = Form(""),
    fuel_consumption: str = Form(""),
    notes: str = Form("")
):

    db = SessionLocal()

    try:
        receipt_document = receipt_document.strip()
        model = model.strip()
        registration_number = registration_number.strip()
        chassis_number = chassis_number.strip()
        status = status.strip()
        department = department.strip()
        fuel_type = fuel_type.strip()
        fuel_consumption = fuel_consumption.strip()
        notes = notes.strip()

        equipment_types = (
            db.query(EquipmentType)
            .order_by(EquipmentType.name)
            .all()
        )

        if not receipt_document:
            return templates.TemplateResponse(
                request=request,
                name="pages/equipment_form.html",
                context={
                    "equipment_types": equipment_types,
                    "error": "وثيقة الاستلام مطلوبة."
                },
                status_code=400
            )

        if not registration_number:
            return templates.TemplateResponse(
                request=request,
                name="pages/equipment_form.html",
                context={
                    "equipment_types": equipment_types,
                    "error": "رقم التسجيل مطلوب."
                },
                status_code=400
            )

        equipment_type = (
            db.query(EquipmentType)
            .filter(
                EquipmentType.id == equipment_type_id
            )
            .first()
        )

        if equipment_type is None:
            return templates.TemplateResponse(
                request=request,
                name="pages/equipment_form.html",
                context={
                    "equipment_types": equipment_types,
                    "error": "نوع العتاد غير موجود."
                },
                status_code=400
            )

        existing_registration = (
            db.query(Equipment)
            .filter(
                Equipment.registration_number
                == registration_number
            )
            .first()
        )

        if existing_registration:
            return templates.TemplateResponse(
                request=request,
                name="pages/equipment_form.html",
                context={
                    "equipment_types": equipment_types,
                    "error": "رقم التسجيل موجود مسبقًا."
                },
                status_code=400
            )

        existing_receipt = (
            db.query(Equipment)
            .filter(
                Equipment.receipt_document
                == receipt_document
            )
            .first()
        )

        if existing_receipt:
            return templates.TemplateResponse(
                request=request,
                name="pages/equipment_form.html",
                context={
                    "equipment_types": equipment_types,
                    "error": "وثيقة الاستلام مستخدمة مسبقًا."
                },
                status_code=400
            )

        new_equipment = Equipment(
            receipt_document=receipt_document,
            equipment_type_id=equipment_type_id,
            model=model,
            registration_number=registration_number,
            chassis_number=chassis_number,
            status=status,
            department=department,
            fuel_type=fuel_type,
            fuel_consumption=fuel_consumption,
            notes=notes,
            date_added=date.today()
        )

        db.add(new_equipment)
        db.commit()

        return RedirectResponse(
            url="/equipment",
            status_code=303
        )

    finally:
        db.close()
