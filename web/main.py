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

INDEX_FILE = BASE_DIR / "templates" / "index.html"

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
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
# لوحة التحكم
# =========================================================

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

        batteries = db.execute(
            text("SELECT COUNT(*) FROM batteries")
        ).scalar() or 0

        tires = db.execute(
            text("SELECT COUNT(*) FROM tires")
        ).scalar() or 0

        open_faults = 0

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


# =========================================================
# قائمة السيارات والعتاد
# =========================================================

@app.get("/equipment")
def equipment_page(request: Request):

    db = None

    try:

        db = SessionLocal()

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

        if db is not None:
            db.close()


# =========================================================
# إضافة عتاد - صفحة النموذج
# =========================================================

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

    db = None

    try:

        db = SessionLocal()

        # -------------------------------------------------
        # تنظيف البيانات
        # -------------------------------------------------

        receipt_document = receipt_document.strip()

        model = model.strip()

        registration_number = registration_number.strip()

        chassis_number = chassis_number.strip()

        status = status.strip()

        department = department.strip()

        fuel_type = fuel_type.strip()

        fuel_consumption = fuel_consumption.strip()

        notes = notes.strip()


        # -------------------------------------------------
        # التحقق من وثيقة الاستلام
        # -------------------------------------------------

        if not receipt_document:

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
                    "error": "وثيقة الاستلام مطلوبة."
                },
                status_code=400
            )


        # -------------------------------------------------
        # التحقق من نوع العتاد
        # -------------------------------------------------

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


        # -------------------------------------------------
        # التحقق من رقم التسجيل
        # -------------------------------------------------

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


        # -------------------------------------------------
        # منع تكرار رقم التسجيل
        # -------------------------------------------------

        existing_registration = (
            db.query(Equipment)
            .filter(
                Equipment.registration_number
                == registration_number
            )
            .first()
        )

        if existing_registration:

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


        # -------------------------------------------------
        # منع تكرار وثيقة الاستلام
        # -------------------------------------------------

        existing_receipt = (
            db.query(Equipment)
            .filter(
                Equipment.receipt_document
                == receipt_document
            )
            .first()
        )

        if existing_receipt:

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
                    "error": "وثيقة الاستلام موجودة مسبقًا."
                },
                status_code=400
            )


        # -------------------------------------------------
        # تحويل معدل الاستهلاك إلى رقم
        # -------------------------------------------------

        consumption = None

        if fuel_consumption:

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


        # -------------------------------------------------
        # إنشاء العتاد
        # -------------------------------------------------

        equipment = Equipment(

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


# =========================================================
# إدارة أنواع العتاد
# =========================================================

@app.get("/equipment-types")
def equipment_types_page(
    request: Request,
    message: str = None,
    error: str = None
):

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
            name="pages/equipment_types.html",
            context={
                "equipment_types": equipment_types,
                "message": message,
                "error": error
            }
        )

    finally:

        if db is not None:
            db.close()


# =========================================================
# صفحة إضافة نوع عتاد
# =========================================================

@app.get("/equipment-types/new")
def new_equipment_type_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="pages/equipment_type_form.html",
        context={
            "error": None
        }
    )


# =========================================================
# حفظ نوع العتاد
# =========================================================

@app.post("/equipment-types/new")
def create_equipment_type(

    request: Request,

    name: str = Form(...),

    description: str = Form("")

):

    db = None

    try:

        db = SessionLocal()

        name = name.strip()

        description = description.strip()


        # -------------------------------------------------
        # التحقق من الاسم
        # -------------------------------------------------

        if not name:

            return templates.TemplateResponse(
                request=request,
                name="pages/equipment_type_form.html",
                context={
                    "error": "اسم نوع العتاد مطلوب."
                },
                status_code=400
            )


        # -------------------------------------------------
        # منع التكرار
        # -------------------------------------------------

        existing = (
            db.query(EquipmentType)
            .filter(
                EquipmentType.name == name
            )
            .first()
        )

        if existing:

            return templates.TemplateResponse(
                request=request,
                name="pages/equipment_type_form.html",
                context={
                    "error": "هذا النوع موجود مسبقًا."
                },
                status_code=400
            )


        # -------------------------------------------------
        # إنشاء النوع
        # -------------------------------------------------

        equipment_type = EquipmentType(

            name=name,

            description=description or None

        )

        db.add(equipment_type)

        db.commit()


        return RedirectResponse(
            url="/equipment-types",
            status_code=303
        )


    except Exception:

        if db is not None:
            db.rollback()

        raise

    finally:

        if db is not None:
            db.close()


# =========================================================
# حذف نوع العتاد
# =========================================================

@app.post("/equipment-types/{equipment_type_id}/delete")
def delete_equipment_type(

    equipment_type_id: int

):

    db = None

    try:

        db = SessionLocal()

        equipment_type = (
            db.query(EquipmentType)
            .filter(
                EquipmentType.id == equipment_type_id
            )
            .first()
        )


        if equipment_type is None:

            return RedirectResponse(
                url="/equipment-types?error=نوع العتاد غير موجود",
                status_code=303
            )


        # -------------------------------------------------
        # التأكد من أن النوع غير مستخدم
        # -------------------------------------------------

        used = (
            db.query(Equipment)
            .filter(
                Equipment.equipment_type_id
                == equipment_type_id
            )
            .first()
        )


        if used:

            return RedirectResponse(
                url=(
                    "/equipment-types"
                    "?error="
                    "لا يمكن حذف هذا النوع لأنه مرتبط بعتاد موجود"
                ),
                status_code=303
            )


        db.delete(equipment_type)

        db.commit()


        return RedirectResponse(
            url=(
                "/equipment-types"
                "?message=تم حذف نوع العتاد بنجاح"
            ),
            status_code=303
        )


    except Exception:

        if db is not None:
            db.rollback()

        raise

    finally:

        if db is not None:
            db.close()


# =========================================================
# قائمة السائقين
# =========================================================

@app.get("/drivers")
def drivers_page(request: Request):

    db = None

    try:

        db = SessionLocal()

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

        if db is not None:
            db.close()


# =========================================================
# فحص النظام
# =========================================================

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
