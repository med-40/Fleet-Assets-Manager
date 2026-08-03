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
from app.models.mission import Mission
from app.models.maintenance_order import MaintenanceOrder
from app.models.workshop_transfer import WorkshopTransfer


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
                    WHERE status IN ('جارية', 'Active', 'في مهمة')
                """)
            ).scalar() or 0
        except Exception:
            active_missions = 0

        try:
            due_maintenance = db.execute(
                text("""
                    SELECT COUNT(*)
                    FROM maintenance_orders
                    WHERE status IN ('جارية', 'في الصيانة')
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
# قائمة أنواع العتاد
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
            fuel_consumption=(
                float(fuel_consumption)
                if fuel_consumption
                else None
            ),
            notes=notes
        )

        db.add(new_equipment)
        db.commit()

        return RedirectResponse(
            url="/equipment",
            status_code=303
        )

    finally:
        db.close()


# =========================================================
# المهمات - القائمة
# =========================================================

@app.get("/missions")
def missions_page(request: Request):

    db = SessionLocal()

    try:

        missions = (
            db.query(Mission)
            .order_by(Mission.start_date.desc())
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="pages/missions.html",
            context={
                "missions": missions
            }
        )

    finally:
        db.close()


# =========================================================
# السيارات المتاحة للمهمات
# =========================================================

def get_available_equipment(db):

    return (
        db.query(Equipment)
        .filter(
            Equipment.status.in_(
                [
                    "متاحة",
                    "Available",
                    "Active"
                ]
            )
        )
        .order_by(
            Equipment.registration_number
        )
        .all()
    )


# =========================================================
# إضافة مهمة - صفحة النموذج
# =========================================================

@app.get("/missions/new")
def new_mission_page(request: Request):

    db = SessionLocal()

    try:

        equipment_list = get_available_equipment(db)

        drivers = (
            db.query(Driver)
            .filter(
                Driver.qualification_confirmed.is_(True),
                Driver.qualification_level == "جيد"
            )
            .order_by(
                Driver.first_name,
                Driver.last_name
            )
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="pages/mission_form.html",
            context={
                "equipment_list": equipment_list,
                "drivers": drivers,
                "error": None
            }
        )

    finally:
        db.close()


# =========================================================
# إضافة مهمة - حفظ البيانات
# =========================================================

@app.post("/missions/new")
def create_mission(
    request: Request,
    equipment_id: int = Form(...),
    driver_id: int = Form(...),
    crew_leader: str = Form(""),
    destination: str = Form(""),
    start_date: str = Form(...),
    end_date: str = Form(""),
    status: str = Form("Active"),
    notes: str = Form("")
):

    db = SessionLocal()

    try:

        crew_leader = crew_leader.strip()
        destination = destination.strip()
        end_date = end_date.strip()
        notes = notes.strip()

        equipment_list = get_available_equipment(db)

        qualified_drivers = (
            db.query(Driver)
            .filter(
                Driver.qualification_confirmed.is_(True),
                Driver.qualification_level == "جيد"
            )
            .order_by(
                Driver.first_name,
                Driver.last_name
            )
            .all()
        )

        equipment = (
            db.query(Equipment)
            .filter(
                Equipment.id == equipment_id
            )
            .first()
        )

        if equipment is None:
            return templates.TemplateResponse(
                request=request,
                name="pages/mission_form.html",
                context={
                    "equipment_list": equipment_list,
                    "drivers": qualified_drivers,
                    "error": "السيارة / العتاد غير موجود."
                },
                status_code=400
            )

        available_statuses = (
            "متاحة",
            "Available",
            "Active"
        )

        if equipment.status not in available_statuses:
            return templates.TemplateResponse(
                request=request,
                name="pages/mission_form.html",
                context={
                    "equipment_list": equipment_list,
                    "drivers": qualified_drivers,
                    "error": (
                        "لا يمكن إسناد هذه السيارة إلى مهمة. "
                        f"حالتها الحالية: "
                        f"{equipment.status or 'غير محددة'}."
                    )
                },
                status_code=400
            )

        driver = (
            db.query(Driver)
            .filter(
                Driver.id == driver_id,
                Driver.qualification_confirmed.is_(True),
                Driver.qualification_level == "جيد"
            )
            .first()
        )

        if driver is None:
            return templates.TemplateResponse(
                request=request,
                name="pages/mission_form.html",
                context={
                    "equipment_list": equipment_list,
                    "drivers": qualified_drivers,
                    "error": (
                        "لا يمكن اختيار هذا السائق. "
                        "يجب أن يكون مؤهلًا بدرجة جيد "
                        "ومؤكد التأهيل."
                    )
                },
                status_code=400
            )

        try:
            parsed_start_date = date.fromisoformat(
                start_date
            )
        except ValueError:
            return templates.TemplateResponse(
                request=request,
                name="pages/mission_form.html",
                context={
                    "equipment_list": equipment_list,
                    "drivers": qualified_drivers,
                    "error": "تاريخ بداية المهمة غير صحيح."
                },
                status_code=400
            )

        parsed_end_date = None

        if end_date:

            try:
                parsed_end_date = date.fromisoformat(
                    end_date
                )
            except ValueError:
                return templates.TemplateResponse(
                    request=request,
                    name="pages/mission_form.html",
                    context={
                        "equipment_list": equipment_list,
                        "drivers": qualified_drivers,
                        "error": "تاريخ نهاية المهمة غير صحيح."
                    },
                    status_code=400
                )

            if parsed_end_date < parsed_start_date:
                return templates.TemplateResponse(
                    request=request,
                    name="pages/mission_form.html",
                    context={
                        "equipment_list": equipment_list,
                        "drivers": qualified_drivers,
                        "error": (
                            "تاريخ نهاية المهمة لا يمكن "
                            "أن يكون قبل تاريخ البداية."
                        )
                    },
                    status_code=400
                )

        new_mission = Mission(
            equipment_id=equipment_id,
            driver_id=driver_id,
            crew_leader=crew_leader,
            destination=destination,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            status="Active",
            notes=notes
        )

        db.add(new_mission)

        equipment.status = "في مهمة"

        db.commit()

        return RedirectResponse(
            url="/missions",
            status_code=303
        )

    finally:
        db.close()


# =========================================================
# إنهاء المهمة
# =========================================================

@app.post("/missions/{mission_id}/complete")
def complete_mission(mission_id: int):

    db = SessionLocal()

    try:

        mission = (
            db.query(Mission)
            .filter(
                Mission.id == mission_id
            )
            .first()
        )

        if mission is None:
            return RedirectResponse(
                url="/missions",
                status_code=303
            )

        if mission.status in (
            "Completed",
            "منتهية"
        ):
            return RedirectResponse(
                url="/missions",
                status_code=303
            )

        mission.status = "Completed"
        mission.end_date = date.today()

        equipment = (
            db.query(Equipment)
            .filter(
                Equipment.id == mission.equipment_id
            )
            .first()
        )

        if equipment is not None:

            if equipment.status in (
                "في مهمة",
                "On Mission"
            ):
                equipment.status = "متاحة"

        db.commit()

        return RedirectResponse(
            url="/missions",
            status_code=303
        )

    finally:
        db.close()


# =========================================================
# =========================================================
# الصيانة داخل المؤسسة
# =========================================================
# =========================================================
#
# هذا القسم خاص فقط بالصيانة التي تتم داخل المؤسسة.
#
# أمثلة:
# - إصلاح عطل
# - صيانة دورية
# - فحص
# - تشخيص
# - استبدال قطعة
#
# لا توجد هنا ورشة خارجية.
#
# =========================================================


# =========================================================
# قائمة الصيانة
# =========================================================

@app.get("/maintenance")
def maintenance_page(request: Request):

    db = SessionLocal()

    try:

                maintenance_orders = (
            db.query(MaintenanceOrder)
            .order_by(
                MaintenanceOrder.maintenance_date.desc()
            )
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="pages/maintenance.html",
            context={
                "maintenance_orders": maintenance_orders
            }
        )

    finally:
        db.close()


# =========================================================
# إضافة صيانة داخل المؤسسة - صفحة النموذج
# =========================================================

@app.get("/maintenance/new")
def new_maintenance_page(request: Request):

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
            name="pages/maintenance_form.html",
            context={
                "equipment_list": equipment_list,
                "error": None
            }
        )

    finally:
        db.close()


# =========================================================
# إضافة صيانة داخل المؤسسة - حفظ
# =========================================================

@app.post("/maintenance/new")
def create_maintenance(
    request: Request,
    equipment_id: int = Form(...),
    maintenance_type: str = Form(...),
    description: str = Form(""),
    maintenance_date: str = Form(""),
    status: str = Form("جارية"),
    notes: str = Form("")
):

    db = SessionLocal()

    try:

        maintenance_type = maintenance_type.strip()
        description = description.strip()
        maintenance_date = maintenance_date.strip()
        status = status.strip()
        notes = notes.strip()

        equipment_list = (
            db.query(Equipment)
            .order_by(
                Equipment.registration_number
            )
            .all()
        )

        # -------------------------------------------------
        # التحقق من نوع الصيانة
        # -------------------------------------------------

        if not maintenance_type:

            return templates.TemplateResponse(
                request=request,
                name="pages/maintenance_form.html",
                context={
                    "equipment_list": equipment_list,
                    "error": "نوع الصيانة مطلوب."
                },
                status_code=400
            )

        # -------------------------------------------------
        # التحقق من العتاد
        # -------------------------------------------------

        equipment = (
            db.query(Equipment)
            .filter(
                Equipment.id == equipment_id
            )
            .first()
        )

        if equipment is None:

            return templates.TemplateResponse(
                request=request,
                name="pages/maintenance_form.html",
                context={
                    "equipment_list": equipment_list,
                    "error": "السيارة / العتاد غير موجود."
                },
                status_code=400
            )

        # -------------------------------------------------
        # تاريخ الصيانة
        # -------------------------------------------------

        parsed_maintenance_date = date.today()

        if maintenance_date:

            try:

                parsed_maintenance_date = date.fromisoformat(
                    maintenance_date
                )

            except ValueError:

                return templates.TemplateResponse(
                    request=request,
                    name="pages/maintenance_form.html",
                    context={
                        "equipment_list": equipment_list,
                        "error": "تاريخ الصيانة غير صحيح."
                    },
                    status_code=400
                )

        # -------------------------------------------------
        # التحقق من الحالة
        # -------------------------------------------------

        allowed_statuses = (
            "جارية",
            "منتهية",
            "ملغاة"
        )

        if status not in allowed_statuses:

            status = "جارية"

        # -------------------------------------------------
        # إنشاء سجل الصيانة الداخلية
        # -------------------------------------------------

        new_maintenance = MaintenanceOrder(
            equipment_id=equipment_id,
            maintenance_type=maintenance_type,
            description=description,
            maintenance_date=parsed_maintenance_date,
            status=status,
            notes=notes
        )

        db.add(new_maintenance)

        # -------------------------------------------------
        # إذا كانت الصيانة جارية:
        # تغيير حالة العتاد تلقائيًا
        # -------------------------------------------------

        if status == "جارية":

            equipment.status = "في الصيانة"

        elif status == "منتهية":

            new_maintenance.completion_date = date.today()

        db.commit()

        return RedirectResponse(
            url="/maintenance",
            status_code=303
        )

    finally:
        db.close()


# =========================================================
# إنهاء الصيانة الداخلية
# =========================================================

@app.post("/maintenance/{maintenance_id}/complete")
def complete_maintenance(
    maintenance_id: int
):

    db = SessionLocal()

    try:

        maintenance = (
            db.query(MaintenanceOrder)
            .filter(
                MaintenanceOrder.id == maintenance_id
            )
            .first()
        )

        if maintenance is None:

            return RedirectResponse(
                url="/maintenance",
                status_code=303
            )

        # إذا كانت منتهية أصلًا
        if maintenance.status == "منتهية":

            return RedirectResponse(
                url="/maintenance",
                status_code=303
            )

        maintenance.status = "منتهية"
        maintenance.completion_date = date.today()

        equipment = (
            db.query(Equipment)
            .filter(
                Equipment.id == maintenance.equipment_id
            )
            .first()
        )

        if equipment is not None:

            # نعيد العتاد إلى متاحة فقط
            # إذا كان في الصيانة بسبب هذه العملية
            if equipment.status == "في الصيانة":

                equipment.status = "متاحة"

        db.commit()

        return RedirectResponse(
            url="/maintenance",
            status_code=303
        )

    finally:
        db.close()
