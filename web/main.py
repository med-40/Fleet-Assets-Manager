from datetime import date, timedelta
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
from app.models.maintenance_type import MaintenanceType
from app.models.maintenance_schedule import MaintenanceSchedule
from app.models.meter_reading import MeterReading

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
                text(
                    """
                    SELECT COUNT(*)
                    FROM missions
                    WHERE status IN (
                        'جارية',
                        'Active',
                        'في مهمة'
                    )
                    """
                )
            ).scalar() or 0

        except Exception:
            active_missions = 0

        try:
            due_maintenance = db.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM maintenance_orders
                    WHERE status IN (
                        'جارية',
                        'في الصيانة'
                    )
                    """
                )
            ).scalar() or 0

        except Exception:
            due_maintenance = 0

        try:
            monthly_fuel = db.execute(
                text(
                    """
                    SELECT COALESCE(
                        SUM(quantity),
                        0
                    )
                    FROM fuel_logs
                    """
                )
            ).scalar() or 0

        except Exception:
            monthly_fuel = 0

        try:
            batteries = db.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM batteries
                    """
                )
            ).scalar() or 0

        except Exception:
            batteries = 0

        try:
            tires = db.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM tires
                    """
                )
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

        parsed_fuel_consumption = None

        if fuel_consumption:

            try:

                parsed_fuel_consumption = float(
                    fuel_consumption
                )

            except ValueError:

                return templates.TemplateResponse(
                    request=request,
                    name="pages/equipment_form.html",
                    context={
                        "equipment_types": equipment_types,
                        "error": "معدل استهلاك الوقود غير صحيح."
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
            fuel_consumption=parsed_fuel_consumption,
            notes=notes
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
# المهمات - القائمة
# =========================================================

@app.get("/missions")
def missions_page(request: Request):

    db = SessionLocal()

    try:

        missions = (
            db.query(Mission)
            .order_by(
                Mission.start_date.desc()
            )
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

        equipment_list = get_available_equipment(
            db
        )

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

        equipment_list = get_available_equipment(
            db
        )

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

    except Exception:

        db.rollback()
        raise

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

    except Exception:

        db.rollback()
        raise

    finally:
        db.close()


# =========================================================
# الصيانة - القائمة
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
# إضافة صيانة - صفحة النموذج
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
# API:
# خطط الصيانة الخاصة بالعتاد المختار
# =========================================================

@app.get("/maintenance/schedules/{equipment_id}")
def get_equipment_maintenance_schedules(
    equipment_id: int
):

    db = SessionLocal()

    try:

        schedules = (
            db.query(MaintenanceSchedule)
            .filter(
                MaintenanceSchedule.equipment_id
                == equipment_id
            )
            .order_by(
                MaintenanceSchedule.name
            )
            .all()
        )

        return [
            {
                "id": schedule.id,
                "name": schedule.name,
                "interval_km": schedule.interval_km,
                "interval_days": schedule.interval_days,
                "last_maintenance_date": (
                    schedule.last_maintenance_date.isoformat()
                    if schedule.last_maintenance_date
                    else None
                ),
                "last_maintenance_meter": (
                    schedule.last_maintenance_meter
                ),
                "next_due_date": (
                    schedule.next_due_date.isoformat()
                    if schedule.next_due_date
                    else None
                ),
                "next_due_meter": (
                    schedule.next_due_meter
                ),
                "description": schedule.description or ""
            }
            for schedule in schedules
        ]

    finally:
        db.close()


# =========================================================
# إعادة نموذج الصيانة مع خطأ
# =========================================================

def maintenance_error_response(
    request,
    equipment_list,
    error
):

    return templates.TemplateResponse(
        request=request,
        name="pages/maintenance_form.html",
        context={
            "equipment_list": equipment_list,
            "error": error
        },
        status_code=400
    )


# =========================================================
# إيجاد خطة الصيانة حسب ID
# =========================================================

def get_maintenance_schedule(
    db,
    schedule_id
):

    return (
        db.query(MaintenanceSchedule)
        .filter(
            MaintenanceSchedule.id
            == schedule_id
        )
        .first()
    )


# =========================================================
# تحديث خطة الصيانة بعد التنفيذ
# =========================================================

def update_maintenance_schedule_after_completion(
    db,
    schedule,
    completion_date,
    meter_reading
):

    schedule.last_maintenance_date = completion_date

    schedule.last_maintenance_meter = meter_reading

    # -----------------------------------------------------
    # الاستحقاق القادم حسب الأيام
    # -----------------------------------------------------

    if (
        schedule.interval_days is not None
        and schedule.interval_days > 0
    ):

        schedule.next_due_date = (
            completion_date
            + timedelta(
                days=schedule.interval_days
            )
        )

    else:

        schedule.next_due_date = None

    # -----------------------------------------------------
    # الاستحقاق القادم حسب العداد
    # -----------------------------------------------------

    if (
        schedule.interval_km is not None
        and schedule.interval_km > 0
        and meter_reading is not None
    ):

        schedule.next_due_meter = (
            meter_reading
            + schedule.interval_km
        )

    else:

        schedule.next_due_meter = None


# =========================================================
# إضافة قراءة عداد
# =========================================================

def create_meter_reading(
    db,
    equipment_id,
    reading_value,
    reading_date
):

    new_reading = MeterReading(
        equipment_id=equipment_id,
        reading_value=reading_value,
        reading_date=reading_date
    )

    db.add(new_reading)

    db.flush()

    return new_reading


# =========================================================
# الحصول على آخر قراءة عداد
# =========================================================

def get_last_meter_reading(
    db,
    equipment_id
):

    return (
        db.query(MeterReading)
        .filter(
            MeterReading.equipment_id
            == equipment_id
        )
        .order_by(
            MeterReading.reading_value.desc()
        )
        .first()
    )


# =========================================================
# إضافة صيانة داخل المؤسسة - حفظ
# =========================================================

@app.post("/maintenance/new")
def create_maintenance(
    request: Request,
    equipment_id: int = Form(...),
    maintenance_schedule_id: int = Form(...),
    meter_reading: str = Form(""),
    description: str = Form(""),
    maintenance_date: str = Form(""),
    completion_date: str = Form(""),
    status: str = Form("جارية"),
    notes: str = Form("")
):

    db = SessionLocal()

    try:

        description = description.strip()
        maintenance_date = maintenance_date.strip()
        completion_date = completion_date.strip()
        status = status.strip()
        notes = notes.strip()
        meter_reading = meter_reading.strip()

        equipment_list = (
            db.query(Equipment)
            .order_by(
                Equipment.registration_number
            )
            .all()
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

            return maintenance_error_response(
                request,
                equipment_list,
                "السيارة / العتاد غير موجود."
            )

        # -------------------------------------------------
        # التحقق من خطة الصيانة
        # -------------------------------------------------

        schedule = get_maintenance_schedule(
            db=db,
            schedule_id=maintenance_schedule_id
        )

        if schedule is None:

            return maintenance_error_response(
                request,
                equipment_list,
                "خطة الصيانة المحددة غير موجودة."
            )

        # -------------------------------------------------
        # التأكد أن الخطة تخص العتاد المختار
        # -------------------------------------------------

        if schedule.equipment_id != equipment_id:

            return maintenance_error_response(
                request,
                equipment_list,
                (
                    "خطة الصيانة المختارة لا تخص "
                    "العتاد المحدد."
                )
            )

        if not schedule.name.strip():

            return maintenance_error_response(
                request,
                equipment_list,
                "اسم خطة الصيانة غير صالح."
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

            return maintenance_error_response(
                request,
                equipment_list,
                "حالة الصيانة غير صحيحة."
            )

        # -------------------------------------------------
        # تاريخ بداية الصيانة
        # -------------------------------------------------

        parsed_maintenance_date = date.today()

        if maintenance_date:

            try:

                parsed_maintenance_date = (
                    date.fromisoformat(
                        maintenance_date
                    )
                )

            except ValueError:

                return maintenance_error_response(
                    request,
                    equipment_list,
                    "تاريخ الصيانة غير صحيح."
                )

        # -------------------------------------------------
        # تاريخ انتهاء الصيانة
        # -------------------------------------------------

        parsed_completion_date = None

        if completion_date:

            try:

                parsed_completion_date = (
                    date.fromisoformat(
                        completion_date
                    )
                )

            except ValueError:

                return maintenance_error_response(
                    request,
                    equipment_list,
                    "تاريخ انتهاء الصيانة غير صحيح."
                )

            if (
                parsed_completion_date
                < parsed_maintenance_date
            ):

                return maintenance_error_response(
                    request,
                    equipment_list,
                    (
                        "تاريخ انتهاء الصيانة لا يمكن "
                        "أن يكون قبل تاريخ بدايتها."
                    )
                )

        # -------------------------------------------------
        # إذا كانت الصيانة منتهية
        # -------------------------------------------------

        if (
            status == "منتهية"
            and parsed_completion_date is None
        ):

            parsed_completion_date = date.today()

        # -------------------------------------------------
        # قراءة العداد
        # -------------------------------------------------

        parsed_meter_reading = None

        if meter_reading:

            try:

                parsed_meter_reading = int(
                    meter_reading
                )

            except ValueError:

                return maintenance_error_response(
                    request,
                    equipment_list,
                    "قراءة العداد يجب أن تكون رقمًا صحيحًا."
                )

            if parsed_meter_reading < 0:

                return maintenance_error_response(
                    request,
                    equipment_list,
                    "قراءة العداد لا يمكن أن تكون سالبة."
                )

        # -------------------------------------------------
        # الصيانة المنتهية تحتاج قراءة عداد
        # -------------------------------------------------

        if (
            status == "منتهية"
            and parsed_meter_reading is None
        ):

            return maintenance_error_response(
                request,
                equipment_list,
                (
                    "يجب إدخال قراءة العداد عند تسجيل "
                    "الصيانة كمنتهية."
                )
            )

        # -------------------------------------------------
        # منع انخفاض العداد
        # -------------------------------------------------

        if parsed_meter_reading is not None:

            last_meter_reading = get_last_meter_reading(
                db=db,
                equipment_id=equipment_id
            )

            if (
                last_meter_reading is not None
                and parsed_meter_reading
                < last_meter_reading.reading_value
            ):

                return maintenance_error_response(
                    request,
                    equipment_list,
                    (
                        "قراءة العداد الجديدة أقل من آخر "
                        "قراءة مسجلة "
                        f"({last_meter_reading.reading_value} كم)."
                    )
                )

        # -------------------------------------------------
        # إنشاء قراءة العداد
        # -------------------------------------------------

        if parsed_meter_reading is not None:

            create_meter_reading(
                db=db,
                equipment_id=equipment_id,
                reading_value=parsed_meter_reading,
                reading_date=(
                    parsed_completion_date
                    or parsed_maintenance_date
                )
            )

        # -------------------------------------------------
        # إنشاء سجل الصيانة
        # -------------------------------------------------

        new_maintenance = MaintenanceOrder(
            equipment_id=equipment_id,

            # الربط المباشر بالخطة
            maintenance_schedule_id=schedule.id,

            # اسم العملية يبقى محفوظًا في السجل
            maintenance_type=schedule.name.strip(),

            description=description,

            maintenance_date=parsed_maintenance_date,

            completion_date=parsed_completion_date,

            meter_reading=parsed_meter_reading,

            status=status,

            notes=notes
        )

        db.add(new_maintenance)

        # -------------------------------------------------
        # تحديث الخطة عند انتهاء الصيانة
        # -------------------------------------------------

        if status == "منتهية":

            update_maintenance_schedule_after_completion(
                db=db,
                schedule=schedule,
                completion_date=(
                    parsed_completion_date
                    or date.today()
                ),
                meter_reading=parsed_meter_reading
            )

        # -------------------------------------------------
        # حالة العتاد
        # -------------------------------------------------

        if status == "جارية":

            equipment.status = "في الصيانة"

        elif status == "منتهية":

            equipment.status = "متاحة"

        elif status == "ملغاة":

            if equipment.status == "في الصيانة":

                equipment.status = "متاحة"

        # -------------------------------------------------
        # حفظ
        # -------------------------------------------------

        db.commit()

        return RedirectResponse(
            url="/maintenance",
            status_code=303
        )

    except Exception:

        db.rollback()
        raise

    finally:
        db.close()


# =========================================================
# الورشة الخارجية - القائمة
# =========================================================

@app.get("/workshops")
def workshops_page(request: Request):

    db = SessionLocal()

    try:

        transfers = (
            db.query(WorkshopTransfer)
            .order_by(
                WorkshopTransfer.dispatch_date.desc()
            )
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="pages/workshops.html",
            context={
                "transfers": transfers
            }
        )

    finally:
        db.close()


# =========================================================
# إرسال عتاد إلى ورشة خارجية - صفحة النموذج
# =========================================================

@app.get("/workshops/new")
def new_workshop_page(request: Request):

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
            name="pages/workshop_form.html",
            context={
                "equipment_list": equipment_list,
                "error": None
            }
        )

    finally:
        db.close()


# =========================================================
# إرسال عتاد إلى ورشة خارجية - حفظ
# =========================================================

@app.post("/workshops/new")
def create_workshop_transfer(
    request: Request,
    equipment_id: int = Form(...),
    workshop_name: str = Form(...),
    dispatch_document: str = Form(...),
    dispatch_date: str = Form(""),
    expected_return_date: str = Form(""),
    reason: str = Form(""),
    notes: str = Form("")
):

    db = SessionLocal()

    try:

        workshop_name = workshop_name.strip()
        dispatch_document = dispatch_document.strip()
        dispatch_date = dispatch_date.strip()
        expected_return_date = expected_return_date.strip()
        reason = reason.strip()
        notes = notes.strip()

        equipment_list = (
            db.query(Equipment)
            .order_by(
                Equipment.registration_number
            )
            .all()
        )

        if not workshop_name:

            return templates.TemplateResponse(
                request=request,
                name="pages/workshop_form.html",
                context={
                    "equipment_list": equipment_list,
                    "error": "اسم الورشة مطلوب."
                },
                status_code=400
            )

        if not dispatch_document:

            return templates.TemplateResponse(
                request=request,
                name="pages/workshop_form.html",
                context={
                    "equipment_list": equipment_list,
                    "error": "وثيقة الإرسال مطلوبة."
                },
                status_code=400
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
                name="pages/workshop_form.html",
                context={
                    "equipment_list": equipment_list,
                    "error": "السيارة / العتاد غير موجود."
                },
                status_code=400
            )

        if equipment.status not in (
            "متاحة",
            "Available",
            "Active"
        ):

            return templates.TemplateResponse(
                request=request,
                name="pages/workshop_form.html",
                context={
                    "equipment_list": equipment_list,
                    "error": (
                        "لا يمكن إرسال هذا العتاد إلى الورشة "
                        f"لأن حالته الحالية هي: "
                        f"{equipment.status or 'غير محددة'}."
                    )
                },
                status_code=400
            )

        parsed_dispatch_date = date.today()

        if dispatch_date:

            try:

                parsed_dispatch_date = (
                    date.fromisoformat(
                        dispatch_date
                    )
                )

            except ValueError:

                return templates.TemplateResponse(
                    request=request,
                    name="pages/workshop_form.html",
                    context={
                        "equipment_list": equipment_list,
                        "error": "تاريخ الإرسال غير صحيح."
                    },
                    status_code=400
                )

        parsed_expected_return_date = None

        if expected_return_date:

            try:

                parsed_expected_return_date = (
                    date.fromisoformat(
                        expected_return_date
                    )
                )

            except ValueError:

                return templates.TemplateResponse(
                    request=request,
                    name="pages/workshop_form.html",
                    context={
                        "equipment_list": equipment_list,
                        "error": "تاريخ العودة المتوقع غير صحيح."
                    },
                    status_code=400
                )

            if (
                parsed_expected_return_date
                < parsed_dispatch_date
            ):

                return templates.TemplateResponse(
                    request=request,
                    name="pages/workshop_form.html",
                    context={
                        "equipment_list": equipment_list,
                        "error": (
                            "تاريخ العودة المتوقع لا يمكن "
                            "أن يكون قبل تاريخ الإرسال."
                        )
                    },
                    status_code=400
                )

        active_transfer = (
            db.query(WorkshopTransfer)
            .filter(
                WorkshopTransfer.equipment_id
                == equipment_id,
                WorkshopTransfer.status
                == "في الورشة"
            )
            .first()
        )

        if active_transfer:

            return templates.TemplateResponse(
                request=request,
                name="pages/workshop_form.html",
                context={
                    "equipment_list": equipment_list,
                    "error": (
                        "هذا العتاد موجود حاليًا في ورشة "
                        "خارجية ولا يمكن إرساله مرة أخرى."
                    )
                },
                status_code=400
            )

        new_transfer = WorkshopTransfer(
            equipment_id=equipment_id,
            workshop_name=workshop_name,
            dispatch_document=dispatch_document,
            dispatch_date=parsed_dispatch_date,
            expected_return_date=parsed_expected_return_date,
            actual_return_date=None,
            reason=reason,
            status="في الورشة",
            notes=notes
        )

        db.add(new_transfer)

        equipment.status = "في ورشة خارجية"

        db.commit()

        return RedirectResponse(
            url="/workshops",
            status_code=303
        )

    except Exception:

        db.rollback()
        raise

    finally:
        db.close()


# =========================================================
# إرجاع العتاد من الورشة الخارجية
# =========================================================

@app.post("/workshops/{transfer_id}/return")
def return_from_workshop(
    transfer_id: int
):

    db = SessionLocal()

    try:

        transfer = (
            db.query(WorkshopTransfer)
            .filter(
                WorkshopTransfer.id == transfer_id
            )
            .first()
        )

        if transfer is None:

            return RedirectResponse(
                url="/workshops",
                status_code=303
            )

        if transfer.status != "في الورشة":

            return RedirectResponse(
                url="/workshops",
                status_code=303
            )

        transfer.actual_return_date = date.today()

        transfer.status = "عاد من الورشة"

        equipment = (
            db.query(Equipment)
            .filter(
                Equipment.id
                == transfer.equipment_id
            )
            .first()
        )

        if equipment is not None:

            equipment.status = "متاحة"

        db.commit()

        return RedirectResponse(
            url="/workshops",
            status_code=303
        )

    except Exception:

        db.rollback()
        raise

    finally:
        db.close()
