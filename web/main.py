from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from app.database.session import SessionLocal
from app.models.equipment import Equipment
from app.models.equipment_type import EquipmentType


BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_FILE = BASE_DIR / "templates" / "index.html"

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


app = FastAPI(
    title="Fleet Assets Manager",
    description="نظام تسيير الحضيرة",
    version="1.0.0"
)


@app.get("/")
def home():

    return FileResponse(INDEX_FILE)


@app.get("/dashboard")
def dashboard(request: Request):

    db = None

    try:

        db = SessionLocal()

        vehicles = db.execute(
            text("SELECT COUNT(*) FROM equipment")
        ).scalar() or 0

        active_missions = db.execute(
            text("""
                SELECT COUNT(*)
                FROM missions
                WHERE status = 'جارية'
            """)
        ).scalar() or 0

        due_maintenance = db.execute(
            text("""
                SELECT COUNT(*)
                FROM maintenance_orders
            """)
        ).scalar() or 0

        monthly_fuel = db.execute(
            text("""
                SELECT COALESCE(SUM(quantity), 0)
                FROM fuel_logs
            """)
        ).scalar() or 0

        open_faults = 0

        batteries = db.execute(
            text("SELECT COUNT(*) FROM batteries")
        ).scalar() or 0

        tires = db.execute(
            text("SELECT COUNT(*) FROM tires")
        ).scalar() or 0

        expiring_licenses = 0

        return templates.TemplateResponse(
            request=request,
            name="pages/dashboard.html",
            context={
                "vehicles": vehicles,
                "active_missions": active_missions,
                "due_maintenance": due_maintenance,
                "monthly_fuel": monthly_fuel,
                "open_faults": open_faults,
                "batteries": batteries,
                "tires": tires,
                "expiring_licenses": expiring_licenses,
            }
        )

    finally:

        if db is not None:
            db.close()


@app.get("/equipment")
def equipment_page(request: Request):

    db = None

    try:

        db = SessionLocal()

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

        if db is not None:
            db.close()


@app.get("/equipment/new")
def new_equipment_page(request: Request):

    db = None

    try:

        db = SessionLocal()

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

        if db is not None:
            db.close()


@app.post("/equipment/new")
def create_equipment(
    request: Request,

    equipment_type_id: int = Form(...),

    registration_number: str = Form(...),

    chassis_number: str = Form(""),

    model: str = Form(""),

    fuel_type: str = Form(""),

    fuel_consumption: str = Form(""),

    status: str = Form("متاحة"),

    department: str = Form(""),
):

    db = None

    try:

        db = SessionLocal()

        registration_number = registration_number.strip()

        chassis_number = chassis_number.strip()

        model = model.strip()

        fuel_type = fuel_type.strip()

        department = department.strip()


        # التأكد من وجود نوع العتاد

        equipment_type = (
            db.query(EquipmentType)
            .filter(
                EquipmentType.id == equipment_type_id
            )
            .first()
        )

        if equipment_type is None:

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
                    "error": "نوع العتاد غير موجود."
                },
                status_code=400
            )


        # التأكد من رقم التسجيل

        if not registration_number:

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
                    "error": "رقم التسجيل مطلوب."
                },
                status_code=400
            )


        existing = (
            db.query(Equipment)
            .filter(
                Equipment.registration_number
                == registration_number
            )
            .first()
        )

        if existing:

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
                    "error": "رقم التسجيل موجود مسبقًا."
                },
                status_code=400
            )


        # تحويل معدل الاستهلاك إلى رقم

        consumption = None

        if fuel_consumption.strip():

            try:

                consumption = float(
                    fuel_consumption.replace(",", ".")
                )

            except ValueError:

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
                        "error": "معدل الاستهلاك يجب أن يكون رقمًا."
                    },
                    status_code=400
                )


        equipment = Equipment(

            equipment_type_id=equipment_type_id,

            receipt_document="غير محدد",

            registration_number=registration_number,

            chassis_number=chassis_number or None,

            model=model or None,

            fuel_type=fuel_type or None,

            fuel_consumption=consumption,

            status=status.strip() or "متاحة",

            department=department or None

        )


        db.add(equipment)

        db.commit()


        return RedirectResponse(
            url="/equipment",
            status_code=303
        )


    except Exception:

        if db is not None:
            db.rollback()

        raise


    finally:

        if db is not None:
            db.close()


@app.get("/health")
def health_check():

    db = None

    try:

        db = SessionLocal()

        db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception as error:

        return {
            "status": "error",
            "database": "disconnected",
            "message": str(error)
        }

    finally:

        if db is not None:
            db.close()
