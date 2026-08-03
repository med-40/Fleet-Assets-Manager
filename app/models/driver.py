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
# فحص الصحة
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


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
        expiring_licenses = 0

        try:

            vehicles = db.execute(
                text(
                    "SELECT COUNT(*) FROM equipment"
                )
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

        try:

            expiring_licenses = db.execute(
                text("""
                    SELECT COUNT(*)
                    FROM drivers
                    WHERE license_expiry_date IS NOT NULL
                    AND license_expiry_date <= DATE('now', '+30 days')
                """)
            ).scalar() or 0

        except Exception:

            expiring_licenses = 0

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
                "expiring_licenses": expiring_licenses,
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
            .order_by(
                Equipment.registration_number
            )
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
# قائمة أنواع العتاد
# =========================================================

@app.get("/equipment-types")
def equipment_types_list():

    db = SessionLocal()

    try:

        equipment_types = (
            db.query(EquipmentType)
            .order_by(
                EquipmentType.name
            )
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
            .order_by(
                EquipmentType.name
            )
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
            .order_by(
                EquipmentType.name
            )
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

        consumption = None

        if fuel_consumption:

            try:

                consumption = float(
                    fuel_consumption.replace(",", ".")
                )

            except ValueError:

                return templates.TemplateResponse(
                    request=request,
                    name="pages/equipment_form.html",
                    context={
                        "equipment_types": equipment_types,
                        "error": "معدل الاستهلاك يجب أن يكون رقمًا."
                    },
                    status_code=400
                )

        new_equipment = Equipment(

            receipt_document=receipt_document,

            equipment_type_id=equipment_type_id,

            model=model or None,

            registration_number=registration_number,

            chassis_number=chassis_number or None,

            status=status or "متاحة",

            department=department or None,

            fuel_type=fuel_type or None,

            fuel_consumption=consumption,

            notes=notes or None

        )

        db.add(new_equipment)

        db.commit()

        return RedirectResponse(
            url="/equipment",
            status_code=303
        )

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# =========================================================
# قائمة السائقين
# =========================================================

@app.get("/drivers")
def drivers_page(request: Request):

    db = SessionLocal()

    try:

        drivers = (
            db.query(Driver)
            .order_by(
                Driver.last_name,
                Driver.first_name
            )
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="pages/drivers.html",
            context={
                "drivers": drivers
            }
        )

    finally:

        db.close()


# =========================================================
# صفحة إضافة سائق
# =========================================================

@app.get("/drivers/new")
def new_driver_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="pages/driver_form.html",
        context={
            "error": None
        }
    )


# =========================================================
# حفظ سائق جديد
# =========================================================

@app.post("/drivers/new")
def create_driver(

    request: Request,

    first_name: str = Form(...),

    last_name: str = Form(...),

    rank: str = Form(""),

    phone: str = Form(""),

    license_number: str = Form(""),

    license_expiry_date: str = Form(""),

    status: str = Form("Active"),

    qualification_confirmed: str = Form("false"),

    qualification_level: str = Form("")

):

    db = SessionLocal()

    try:

        first_name = first_name.strip()
        last_name = last_name.strip()
        rank = rank.strip()
        phone = phone.strip()
        license_number = license_number.strip()
        license_expiry_date = license_expiry_date.strip()
        status = status.strip()

        qualification_confirmed = (
            qualification_confirmed.strip().lower()
        )

        qualification_level = (
            qualification_level.strip()
        )

        if not first_name:

            return templates.TemplateResponse(
                request=request,
                name="pages/driver_form.html",
                context={
                    "error": "الاسم مطلوب."
                },
                status_code=400
            )

        if not last_name:

            return templates.TemplateResponse(
                request=request,
                name="pages/driver_form.html",
                context={
                    "error": "اللقب مطلوب."
                },
                status_code=400
            )

        # -------------------------------------------------
        # تحويل قيمة التأكيد إلى Boolean
        # -------------------------------------------------

        confirmed = qualification_confirmed in (
            "true",
            "1",
            "yes",
            "on",
            "نعم"
        )

        # -------------------------------------------------
        # التأهيل
        #
        # إذا لم يجتز مرحلة التأكيد:
        # يعتبر غير مؤهل مهما كانت القيمة المرسلة.
        # -------------------------------------------------

        allowed_levels = {
            "سيئ",
            "حسن",
            "جيد"
        }

        if not confirmed:

            qualification_level = None

        elif qualification_level not in allowed_levels:

            return templates.TemplateResponse(
                request=request,
                name="pages/driver_form.html",
                context={
                    "error": (
                        "يجب تحديد درجة التأهيل: "
                        "سيئ أو حسن أو جيد."
                    )
                },
                status_code=400
            )

        # -------------------------------------------------
        # التحقق من رقم رخصة السياقة
        # -------------------------------------------------

        if license_number:

            existing_license = (
                db.query(Driver)
                .filter(
                    Driver.license_number
                    == license_number
                )
                .first()
            )

            if existing_license:

                return templates.TemplateResponse(
                    request=request,
                    name="pages/driver_form.html",
                    context={
                        "error": (
                            "رقم رخصة السياقة "
                            "موجود مسبقًا."
                        )
                    },
                    status_code=400
                )

        # -------------------------------------------------
        # تاريخ انتهاء الرخصة
        # -------------------------------------------------

        expiry_date = None

        if license_expiry_date:

            try:

                expiry_date = date.fromisoformat(
                    license_expiry_date
                )

            except ValueError:

                return templates.TemplateResponse(
                    request=request,
                    name="pages/driver_form.html",
                    context={
                        "error": (
                            "تاريخ انتهاء الرخصة "
                            "غير صحيح."
                        )
                    },
                    status_code=400
                )

        # -------------------------------------------------
        # إنشاء السائق
        # -------------------------------------------------

        driver = Driver(

            first_name=first_name,

            last_name=last_name,

            rank=rank or None,

            phone=phone or None,

            license_number=license_number or None,

            license_expiry_date=expiry_date,

            status=status or "Active",

            qualification_confirmed=confirmed,

            qualification_level=(
                qualification_level
                if confirmed
                else None
            )

        )

        db.add(driver)

        db.commit()

        return RedirectResponse(
            url="/drivers",
            status_code=303
        )

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()
