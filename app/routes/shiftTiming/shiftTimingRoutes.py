from fastapi import APIRouter, Depends, HTTPException
from app.config.db_config import get_db
from app.schema.shiftTiming import ShiftTiming
from sqlalchemy.orm import Session
from app.models.shiftTimingBase import ShiftTimingResponse,ShiftTimingUpdate
from typing import List
from app.controllers.shiftTimings.shiftTimingsController import getShiftTimingsController,updateShiftTimingsController

shiftTimings_router=APIRouter()

@shiftTimings_router.get("/shiftTimings",response_model=List[ShiftTimingResponse])
def getShiftTimingsRoute(db: Session = Depends(get_db)):
    return getShiftTimingsController(db)

@shiftTimings_router.put("/shiftTimings",response_model=List[ShiftTimingResponse])
def updateShiftTimingsRoute(shift_timings:List[ShiftTimingUpdate],db: Session = Depends(get_db)):
    return updateShiftTimingsController(db,shift_timings)