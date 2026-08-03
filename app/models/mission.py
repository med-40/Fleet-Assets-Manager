from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.database.base import Base

Mission = type(
"Mission",
(Base,),
{
"tablename": "missions",

    "id": Column(
        Integer,
        primary_key=True
    ),

    "equipment_id": Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False
    ),

    "driver_id": Column(
        Integer,
        ForeignKey("drivers.id")
    ),

    "crew_leader": Column(
        String(200)
    ),

    "destination": Column(
        String(200)
    ),

    "start_date": Column(
        Date,
        nullable=False
    ),

    "end_date": Column(
        Date
    ),

    "status": Column(
        String(50),
        default="Active"
    ),

    "notes": Column(
        String(500)
    )
}

)
