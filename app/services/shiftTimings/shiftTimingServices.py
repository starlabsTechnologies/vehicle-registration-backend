from sqlalchemy.orm import Session
from app.schema.shiftTiming import ShiftTiming
from app.models.shiftTimingBase import ShiftTimingResponse,ShiftTimingUpdate
from app.schema.shiftTimingLogs import ShiftTimingLogs
from typing import List
from enum import Enum

class ActionsTypeEnum(Enum):  # Using Python's Enum class
    DELETED = "DELETED"
    CREATED = "CREATED"
    EDITED = "EDITED"

def getShifts(db:Session) -> List[ShiftTimingResponse] :
    shift_timings=db.query(ShiftTiming).all()
    return [
        ShiftTimingResponse(
            id=str(shift.id),
            shift_name=shift.shift_name,
            from_time=shift.from_time,
            to_time=shift.to_time,
            createdAt=shift.createdAt,
            updatedAt=shift.updatedAt
        ) for shift in shift_timings
    ]

def updateShifts(db:Session,shift_timings: List[ShiftTimingUpdate]) -> bool :
    for shifts in shift_timings:
        shift=db.query(ShiftTiming).filter(shifts.shift_name==ShiftTiming.shift_name).first()

        if shift is None:
            return False
        
        shift.shift_name=shifts.shift_name if shifts.shift_name is not None else shift.shift_name
        shift.from_time=shifts.from_time if shifts.from_time is not None else shift.from_time
        shift.to_time=shifts.to_time if shifts.to_time is not None else shift.to_time

        db.commit()
        db.refresh(shift)

    return True

def updateShiftTimingsLogs(shift_timings: List[ShiftTimingUpdate],db:Session,actionByUsername:str) -> bool:
    newShift = [
        ShiftTimingLogs(
            shift_name=shift_timings[0].shift_name,
            from_time=shift_timings[0].from_time,
            to_time=shift_timings[0].to_time,
            action=ActionsTypeEnum.EDITED.value,
            actionBy=actionByUsername
        ),
        ShiftTimingLogs(
            shift_name=shift_timings[1].shift_name,
            from_time=shift_timings[1].from_time,
            to_time=shift_timings[1].to_time,
            action=ActionsTypeEnum.EDITED.value,
            actionBy=actionByUsername
        ),
        ShiftTimingLogs(
            shift_name=shift_timings[2].shift_name,
            from_time=shift_timings[2].from_time,
            to_time=shift_timings[2].to_time,
            action=ActionsTypeEnum.EDITED.value,
            actionBy=actionByUsername
        )]

    db.add_all(newShift)
    db.commit()

    if(newShift):
        return True
    
    return False