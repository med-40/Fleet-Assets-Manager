from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db

from .schemas import (
    MaintenanceOrderCreate,
    MaintenanceOrderRead,
    MaintenanceOrderUpdate,
    MaintenanceScheduleCreate,
    MaintenanceScheduleRead,
    MaintenanceScheduleUpdate,
    MaintenanceTypeCreate,
    MaintenanceTypeRead,
    MaintenanceTypeUpdate,
    MeterReadingCreate,
    MeterReadingRead,
    MeterReadingUpdate,
)

from .service import (
    complete_maintenance_order,
    create_maintenance_order,
    create_maintenance_schedule,
    create_maintenance_type,
    create_meter_reading,
    get_due_schedules,
    get_equipment_maintenance_orders,
    get_equipment_schedules,
    get_last_meter_reading,
    get_maintenance_order,
    get_maintenance_schedule,
    update_maintenance_schedule,
    update_maintenance_type,
)


router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"],
)


# =========================================================
# أنواع الصيانة
# =========================================================

@router.post(
    "/types",
    response_model=MaintenanceTypeRead,
)
def create_type(
    data: MaintenanceTypeCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_maintenance_type(
            db=db,
            name=data.name,
            description=data.description,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.put(
    "/types/{maintenance_type_id}",
    response_model=MaintenanceTypeRead,
)
def update_type(
    maintenance_type_id: int,
    data: MaintenanceTypeUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_maintenance_type(
            db=db,
            maintenance_type_id=maintenance_type_id,
            name=data.name,
            description=data.description,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# =========================================================
# خطط الصيانة
# =========================================================

@router.post(
    "/schedules",
    response_model=MaintenanceScheduleRead,
)
def create_schedule(
    data: MaintenanceScheduleCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_maintenance_schedule(
            db=db,
            equipment_id=data.equipment_id,
            name=data.name,
            interval_km=data.interval_km,
            interval_days=data.interval_days,
            description=data.description,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/schedules/{schedule_id}",
    response_model=MaintenanceScheduleRead,
)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
):
    schedule = get_maintenance_schedule(
        db,
        schedule_id,
    )

    if schedule is None:
        raise HTTPException(
            status_code=404,
            detail="خطة الصيانة غير موجودة.",
        )

    return schedule


@router.get(
    "/equipment/{equipment_id}/schedules",
    response_model=list[MaintenanceScheduleRead],
)
def get_schedules_for_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    return get_equipment_schedules(
        db,
        equipment_id,
    )


@router.put(
    "/schedules/{schedule_id}",
    response_model=MaintenanceScheduleRead,
)
def update_schedule(
    schedule_id: int,
    data: MaintenanceScheduleUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_maintenance_schedule(
            db=db,
            schedule_id=schedule_id,
            name=data.name,
            interval_km=data.interval_km,
            interval_days=data.interval_days,
            description=data.description,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# =========================================================
# قراءات العداد
# =========================================================

@router.post(
    "/meter-readings",
    response_model=MeterReadingRead,
)
def create_reading(
    data: MeterReadingCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_meter_reading(
            db=db,
            equipment_id=data.equipment_id,
            reading_value=data.reading_value,
            reading_date=data.reading_date,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/equipment/{equipment_id}/meter-reading",
    response_model=Optional[MeterReadingRead],
)
def get_last_reading(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    return get_last_meter_reading(
        db,
        equipment_id,
    )


# =========================================================
# أوامر الصيانة
# =========================================================

@router.post(
    "/orders",
    response_model=MaintenanceOrderRead,
)
def create_order(
    data: MaintenanceOrderCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_maintenance_order(
            db=db,
            equipment_id=data.equipment_id,
            maintenance_type=data.maintenance_type,
            maintenance_schedule_id=(
                data.maintenance_schedule_id
            ),
            description=data.description,
            maintenance_date=data.maintenance_date,
            completion_date=data.completion_date,
            meter_reading=data.meter_reading,
            status=data.status,
            notes=data.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/orders/{order_id}",
    response_model=MaintenanceOrderRead,
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = get_maintenance_order(
        db,
        order_id,
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="سجل الصيانة غير موجود.",
        )

    return order


@router.get(
    "/equipment/{equipment_id}/orders",
    response_model=list[MaintenanceOrderRead],
)
def get_equipment_orders(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    return get_equipment_maintenance_orders(
        db,
        equipment_id,
    )


# =========================================================
# إتمام الصيانة
# =========================================================

@router.post(
    "/orders/{order_id}/complete",
    response_model=MaintenanceOrderRead,
)
def complete_order(
    order_id: int,
    completion_date: Optional[date] = Query(
        default=None
    ),
    meter_reading: Optional[int] = Query(
        default=None,
        ge=0,
    ),
    db: Session = Depends(get_db),
):
    try:
        return complete_maintenance_order(
            db=db,
            order_id=order_id,
            completion_date=completion_date,
            meter_reading=meter_reading,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# =========================================================
# الصيانة المستحقة
# =========================================================

@router.get(
    "/due",
    response_model=list[MaintenanceScheduleRead],
)
def get_due_maintenance(
    db: Session = Depends(get_db),
):
    return get_due_schedules(db)
