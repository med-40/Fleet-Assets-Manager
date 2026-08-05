from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =========================================================
# Maintenance Type
# =========================================================

class MaintenanceTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(
        default=None,
        max_length=300
    )


class MaintenanceTypeCreate(MaintenanceTypeBase):
    pass


class MaintenanceTypeUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    description: Optional[str] = Field(
        default=None,
        max_length=300
    )


class MaintenanceTypeRead(MaintenanceTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# =========================================================
# Maintenance Schedule
# =========================================================

class MaintenanceScheduleBase(BaseModel):
    equipment_id: int
    name: str = Field(..., min_length=1, max_length=150)

    interval_km: Optional[int] = Field(
        default=None,
        ge=0
    )

    interval_days: Optional[int] = Field(
        default=None,
        ge=0
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )


class MaintenanceScheduleCreate(MaintenanceScheduleBase):
    pass


class MaintenanceScheduleUpdate(BaseModel):
    equipment_id: Optional[int] = None

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=150
    )

    interval_km: Optional[int] = Field(
        default=None,
        ge=0
    )

    interval_days: Optional[int] = Field(
        default=None,
        ge=0
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )


class MaintenanceScheduleRead(MaintenanceScheduleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    last_maintenance_date: Optional[date] = None
    last_maintenance_meter: Optional[int] = None

    next_due_date: Optional[date] = None
    next_due_meter: Optional[int] = None


# =========================================================
# Maintenance Order
# =========================================================

class MaintenanceOrderBase(BaseModel):
    equipment_id: int

    maintenance_schedule_id: Optional[int] = None

    maintenance_type: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    maintenance_date: Optional[date] = None

    completion_date: Optional[date] = None

    meter_reading: Optional[int] = Field(
        default=None,
        ge=0
    )

    status: str = Field(
        default="جارية",
        min_length=1,
        max_length=50
    )

    notes: Optional[str] = Field(
        default=None,
        max_length=500
    )


class MaintenanceOrderCreate(MaintenanceOrderBase):
    pass


class MaintenanceOrderUpdate(BaseModel):
    maintenance_schedule_id: Optional[int] = None

    maintenance_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    maintenance_date: Optional[date] = None

    completion_date: Optional[date] = None

    meter_reading: Optional[int] = Field(
        default=None,
        ge=0
    )

    status: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    notes: Optional[str] = Field(
        default=None,
        max_length=500
    )


class MaintenanceOrderRead(MaintenanceOrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# =========================================================
# Meter Reading
# =========================================================

class MeterReadingBase(BaseModel):
    equipment_id: int

    reading_value: int = Field(
        ...,
        ge=0
    )

    reading_date: date


class MeterReadingCreate(MeterReadingBase):
    pass


class MeterReadingUpdate(BaseModel):
    reading_value: Optional[int] = Field(
        default=None,
        ge=0
    )

    reading_date: Optional[date] = None


class MeterReadingRead(MeterReadingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
