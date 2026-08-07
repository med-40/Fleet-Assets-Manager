from datetime import date, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from .models import (
    MaintenanceOrder,
    MaintenanceSchedule,
    MaintenanceType,
    MeterReading,
)


# =========================================================
# الحالات المسموح بها
# =========================================================

MAINTENANCE_STATUSES = (
    "جارية",
    "منتهية",
    "ملغاة",
)


# =========================================================
# أنواع الصيانة
# =========================================================

def create_maintenance_type(
    db: Session,
    name: str,
    description: Optional[str] = None,
):
    name = name.strip()

    if not name:
        raise ValueError("اسم نوع الصيانة مطلوب.")

    existing = (
        db.query(MaintenanceType)
        .filter(MaintenanceType.name == name)
        .first()
    )

    if existing:
        raise ValueError("نوع الصيانة موجود مسبقًا.")

    item = MaintenanceType(
        name=name,
        description=description.strip()
        if description
        else None,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def update_maintenance_type(
    db: Session,
    maintenance_type_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
):
    item = (
        db.query(MaintenanceType)
        .filter(MaintenanceType.id == maintenance_type_id)
        .first()
    )

    if item is None:
        raise ValueError("نوع الصيانة غير موجود.")

    if name is not None:
        name = name.strip()

        if not name:
            raise ValueError("اسم نوع الصيانة مطلوب.")

        duplicate = (
            db.query(MaintenanceType)
            .filter(
                MaintenanceType.name == name,
                MaintenanceType.id != maintenance_type_id,
            )
            .first()
        )

        if duplicate:
            raise ValueError("نوع الصيانة موجود مسبقًا.")

        item.name = name

    if description is not None:
        item.description = description.strip()

    db.commit()
    db.refresh(item)

    return item


# =========================================================
# خطط الصيانة
# =========================================================

def create_maintenance_schedule(
    db: Session,
    equipment_id: int,
    name: str,
    interval_km: Optional[int] = None,
    interval_days: Optional[int] = None,
    description: Optional[str] = None,
):
    name = name.strip()

    if not name:
        raise ValueError("اسم خطة الصيانة مطلوب.")

    if interval_km is None and interval_days is None:
        raise ValueError(
            "يجب تحديد شرط الصيانة بالعداد أو بالأيام."
        )

    if interval_km is not None and interval_km < 0:
        raise ValueError("فترة العداد غير صحيحة.")

    if interval_days is not None and interval_days < 0:
        raise ValueError("فترة الأيام غير صحيحة.")

    schedule = MaintenanceSchedule(
        equipment_id=equipment_id,
        name=name,
        interval_km=interval_km,
        interval_days=interval_days,
        description=description.strip()
        if description
        else None,
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return schedule


def get_maintenance_schedule(
    db: Session,
    schedule_id: int,
):
    return (
        db.query(MaintenanceSchedule)
        .filter(MaintenanceSchedule.id == schedule_id)
        .first()
    )


def get_equipment_schedules(
    db: Session,
    equipment_id: int,
):
    return (
        db.query(MaintenanceSchedule)
        .filter(
            MaintenanceSchedule.equipment_id == equipment_id
        )
        .order_by(MaintenanceSchedule.name)
        .all()
    )


def update_maintenance_schedule(
    db: Session,
    schedule_id: int,
    name: Optional[str] = None,
    interval_km: Optional[int] = None,
    interval_days: Optional[int] = None,
    description: Optional[str] = None,
):
    schedule = get_maintenance_schedule(
        db,
        schedule_id,
    )

    if schedule is None:
        raise ValueError("خطة الصيانة غير موجودة.")

    if name is not None:
        name = name.strip()

        if not name:
            raise ValueError("اسم خطة الصيانة مطلوب.")

        schedule.name = name

    if interval_km is not None and interval_km < 0:
        raise ValueError("فترة العداد غير صحيحة.")

    if interval_days is not None and interval_days < 0:
        raise ValueError("فترة الأيام غير صحيحة.")

    if interval_km is not None:
        schedule.interval_km = interval_km

    if interval_days is not None:
        schedule.interval_days = interval_days

    if (
        schedule.interval_km is None
        and schedule.interval_days is None
    ):
        raise ValueError(
            "يجب أن تحتوي الخطة على شرط عداد أو أيام."
        )

    if description is not None:
        schedule.description = description.strip()

    db.commit()
    db.refresh(schedule)

    return schedule


# =========================================================
# قراءة العداد
# =========================================================

def get_last_meter_reading(
    db: Session,
    equipment_id: int,
):
    return (
        db.query(MeterReading)
        .filter(
            MeterReading.equipment_id == equipment_id
        )
        .order_by(
            MeterReading.reading_date.desc(),
            MeterReading.id.desc(),
        )
        .first()
    )


def create_meter_reading(
    db: Session,
    equipment_id: int,
    reading_value: int,
    reading_date: date,
):
    if reading_value < 0:
        raise ValueError(
            "قراءة العداد لا يمكن أن تكون سالبة."
        )

    last_reading = get_last_meter_reading(
        db,
        equipment_id,
    )

    if (
        last_reading is not None
        and reading_value < last_reading.reading_value
    ):
        raise ValueError(
            "قراءة العداد الجديدة أقل من آخر قراءة."
        )

    reading = MeterReading(
        equipment_id=equipment_id,
        reading_value=reading_value,
        reading_date=reading_date,
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    return reading


# =========================================================
# حساب الاستحقاق القادم
# =========================================================

def update_schedule_after_completion(
    schedule: MaintenanceSchedule,
    completion_date: date,
    meter_reading: Optional[int],
):
    schedule.last_maintenance_date = completion_date
    schedule.last_maintenance_meter = meter_reading

    if (
        schedule.interval_days is not None
        and schedule.interval_days > 0
    ):
        schedule.next_due_date = (
            completion_date
            + timedelta(days=schedule.interval_days)
        )
    else:
        schedule.next_due_date = None

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
# أوامر الصيانة
# =========================================================

def create_maintenance_order(
    db: Session,
    equipment_id: int,
    maintenance_type: str,
    maintenance_schedule_id: Optional[int] = None,
    description: Optional[str] = None,
    maintenance_date: Optional[date] = None,
    completion_date: Optional[date] = None,
    meter_reading: Optional[int] = None,
    status: str = "جارية",
    notes: Optional[str] = None,
):
    maintenance_type = maintenance_type.strip()
    status = status.strip()

    if not maintenance_type:
        raise ValueError("نوع الصيانة مطلوب.")

    if status not in MAINTENANCE_STATUSES:
        raise ValueError("حالة الصيانة غير صحيحة.")

    if maintenance_date is None:
        maintenance_date = date.today()

    if completion_date is not None:
        if completion_date < maintenance_date:
            raise ValueError(
                "تاريخ الانتهاء لا يمكن أن يكون قبل البداية."
            )

    if status == "منتهية" and completion_date is None:
        completion_date = date.today()

    if meter_reading is not None:
        if meter_reading < 0:
            raise ValueError(
                "قراءة العداد لا يمكن أن تكون سالبة."
            )

        last_reading = get_last_meter_reading(
            db,
            equipment_id,
        )

        if (
            last_reading is not None
            and meter_reading < last_reading.reading_value
        ):
            raise ValueError(
                "قراءة العداد الجديدة أقل من آخر قراءة."
            )

    schedule = None

    if maintenance_schedule_id is not None:
        schedule = (
            db.query(MaintenanceSchedule)
            .filter(
                MaintenanceSchedule.id
                == maintenance_schedule_id
            )
            .first()
        )

        if schedule is None:
            raise ValueError(
                "خطة الصيانة غير موجودة."
            )

        if schedule.equipment_id != equipment_id:
            raise ValueError(
                "خطة الصيانة لا تخص هذا العتاد."
            )

    order = MaintenanceOrder(
        equipment_id=equipment_id,
        maintenance_schedule_id=maintenance_schedule_id,
        maintenance_type=maintenance_type,
        description=description.strip()
        if description
        else None,
        maintenance_date=maintenance_date,
        completion_date=completion_date,
        meter_reading=meter_reading,
        status=status,
        notes=notes.strip() if notes else None,
    )

    db.add(order)

    if (
        status == "منتهية"
        and schedule is not None
    ):
        update_schedule_after_completion(
            schedule=schedule,
            completion_date=completion_date,
            meter_reading=meter_reading,
        )

    db.commit()
    db.refresh(order)

    return order


def get_maintenance_order(
    db: Session,
    order_id: int,
):
    return (
        db.query(MaintenanceOrder)
        .filter(MaintenanceOrder.id == order_id)
        .first()
    )


def get_equipment_maintenance_orders(
    db: Session,
    equipment_id: int,
):
    return (
        db.query(MaintenanceOrder)
        .filter(
            MaintenanceOrder.equipment_id == equipment_id
        )
        .order_by(
            MaintenanceOrder.maintenance_date.desc()
        )
        .all()
    )


# =========================================================
# إتمام الصيانة
# =========================================================

def complete_maintenance_order(
    db: Session,
    order_id: int,
    completion_date: Optional[date] = None,
    meter_reading: Optional[int] = None,
):
    order = get_maintenance_order(
        db,
        order_id,
    )

    if order is None:
        raise ValueError("سجل الصيانة غير موجود.")

    if order.status == "منتهية":
        return order

    if completion_date is None:
        completion_date = date.today()

    if (
        order.maintenance_date is not None
        and completion_date < order.maintenance_date
    ):
        raise ValueError(
            "تاريخ الانتهاء لا يمكن أن يكون قبل البداية."
        )

    if meter_reading is not None:
        if meter_reading < 0:
            raise ValueError(
                "قراءة العداد لا يمكن أن تكون سالبة."
            )

        last_reading = get_last_meter_reading(
            db,
            order.equipment_id,
        )

        if (
            last_reading is not None
            and meter_reading < last_reading.reading_value
        ):
            raise ValueError(
                "قراءة العداد الجديدة أقل من آخر قراءة."
            )

        reading = MeterReading(
            equipment_id=order.equipment_id,
            reading_value=meter_reading,
            reading_date=completion_date,
        )

        db.add(reading)

    order.status = "منتهية"
    order.completion_date = completion_date

    if meter_reading is not None:
        order.meter_reading = meter_reading

    if order.maintenance_schedule_id is not None:
        schedule = get_maintenance_schedule(
            db,
            order.maintenance_schedule_id,
        )

        if schedule is not None:
            update_schedule_after_completion(
                schedule=schedule,
                completion_date=completion_date,
                meter_reading=order.meter_reading,
            )

    db.commit()
    db.refresh(order)

    return order


# =========================================================
# الصيانة المستحقة
# =========================================================

def get_due_schedules(
    db: Session,
    today: Optional[date] = None,
    current_meter_by_equipment=None,
):
    if today is None:
        today = date.today()

    schedules = (
        db.query(MaintenanceSchedule)
        .all()
    )

    # =====================================================
    # جلب آخر قراءة عداد تلقائيًا
    # =====================================================

    if current_meter_by_equipment is None:

        current_meter_by_equipment = {}

        equipment_ids = {
            schedule.equipment_id
            for schedule in schedules
        }

        for equipment_id in equipment_ids:

            last_reading = get_last_meter_reading(
                db,
                equipment_id,
            )

            if last_reading is not None:
                current_meter_by_equipment[
                    equipment_id
                ] = last_reading.reading_value

    due = []

    for schedule in schedules:

        date_due = (
            schedule.next_due_date is not None
            and schedule.next_due_date <= today
        )

        meter_due = False

        current_meter = (
            current_meter_by_equipment.get(
                schedule.equipment_id
            )
        )

        if (
            schedule.next_due_meter is not None
            and current_meter is not None
        ):
            meter_due = (
                current_meter
                >= schedule.next_due_meter
            )

        if date_due or meter_due:
            due.append(schedule)

    return due
