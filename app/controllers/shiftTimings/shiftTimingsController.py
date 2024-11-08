from app.services.shiftTimings.shiftTimingServices import getShifts, updateShifts
from app.models.shiftTimingBase import ShiftTimingResponse,ShiftTimingUpdate
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import List

def getShiftTimingsController(db:Session) -> List[ShiftTimingResponse] :
    shift_timings=getShifts(db)

    if not shift_timings:
        return JSONResponse(
                content={"message": "No Shift Timings Found"},
                status_code=404
            )
    
    return shift_timings

def updateShiftTimingsController(db:Session,shift_timings: List[ShiftTimingUpdate]) -> List[ShiftTimingResponse] :
    previous_end_time = None
    for shifts in shift_timings:
        from_datetime = datetime.combine(datetime.today(), shifts.from_time)
        to_datetime = datetime.combine(datetime.today(), shifts.to_time)

        time_diff=to_datetime - from_datetime

        if ((time_diff.total_seconds() < 0) and ((from_datetime.hour+8)>24)):
            time_diff = timedelta(days=1) + time_diff 

        if(time_diff < timedelta(hours=7,minutes=59,seconds=59)):
            return JSONResponse(
                content={"message": "Time difference should be exactly 8 hours"},
                status_code=400
            )
        
        if(previous_end_time and shifts.from_time<=previous_end_time):
            return JSONResponse(
                content={"message": "Shift timings shouldnot overlap"},
                status_code=400
            )
        
        previous_end_time=shifts.to_time

    updated=updateShifts(db,shift_timings)

    if not updated:
        return JSONResponse(
                content={"message": "Shift not found"},
                status_code=404
            )
    
    return getShifts(db)