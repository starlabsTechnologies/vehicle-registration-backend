from app.services.shiftTimings.shiftTimingServices import getShifts, updateShifts
from app.models.shiftTimingBase import ShiftTimingResponse,ShiftTimingUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta, time, timezone
from typing import List

def getShiftTimingsController(db:Session) -> List[ShiftTimingResponse] :
    shift_timings=getShifts(db)

    if not shift_timings:
        return HTTPException(status_code=404,detail='No Shift Timings Found')
    
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
            raise HTTPException(status_code=400,detail='Time difference should be exactly 8 hours')
        
        if(previous_end_time and shifts.from_time<=previous_end_time):
            raise HTTPException(status_code=400,detail='Shift timings shouldnot overlap')
        
        previous_end_time=shifts.to_time

    updated=updateShifts(db,shift_timings)

    if not updated:
        raise HTTPException(status_code=404,detail='Shift not found')
    
    return getShifts(db)