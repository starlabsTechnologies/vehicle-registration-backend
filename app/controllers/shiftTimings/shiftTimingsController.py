from app.services.shiftTimings.shiftTimingServices import getShifts, updateShifts
from app.models.shiftTimingBase import ShiftTimingResponse,ShiftTimingUpdate
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import List
from app.utils.logger import logger

def getShiftTimingsController(db:Session) -> List[ShiftTimingResponse] :
    try:
        shift_timings=getShifts(db)

        if not shift_timings:
            logger.warning("No Shift Timings Found")
            return JSONResponse(
                    content={"message": "No Shift Timings Found"},
                    status_code=404
                )
        
        logger.info("Shift Timings fetched successfully")
        return shift_timings
    
    except Exception as error:
        logger.error(f"Error occurred while fetching shift timings: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching shift timings"},
            status_code=500
        )

def updateShiftTimingsController(db:Session,shift_timings: List[ShiftTimingUpdate]) -> List[ShiftTimingResponse] :
    try:
        previous_end_time = None
        for shifts in shift_timings:
            from_datetime = datetime.combine(datetime.today(), shifts.from_time)
            to_datetime = datetime.combine(datetime.today(), shifts.to_time)

            time_diff=to_datetime - from_datetime

            if ((time_diff.total_seconds() < 0) and ((from_datetime.hour+8)>24)):
                time_diff = timedelta(days=1) + time_diff 

            if(time_diff < timedelta(hours=7,minutes=59,seconds=59)):
                logger.warning("Time difference should be exactly 8 hours")
                return JSONResponse(
                    content={"message": "Time difference should be exactly 8 hours"},
                    status_code=400
                )
            
            if(previous_end_time and shifts.from_time<=previous_end_time):
                logger.warning("Shift timings shouldnot overlap")
                return JSONResponse(
                    content={"message": "Shift timings shouldnot overlap"},
                    status_code=400
                )
            
            previous_end_time=shifts.to_time

        updated=updateShifts(db,shift_timings)

        if not updated:
            logger.warning("Shift not found")
            return JSONResponse(
                    content={"message": "Shift not found"},
                    status_code=404
                )
        
        logger.info("Shift timings updated successfully")
        return getShifts(db)
    
    except Exception as error:
        logger.error(f"Error occurred while updating shift timings: {error}")
        return JSONResponse(
            content={"message": "Error occurred while updating shift timings"},
            status_code=500
        )