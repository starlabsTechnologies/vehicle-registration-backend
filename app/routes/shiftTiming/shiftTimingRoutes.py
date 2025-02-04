from fastapi import APIRouter, Depends, Request
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.shiftTimingBase import ShiftTimingResponse,ShiftTimingUpdate
from typing import List
from app.controllers.shiftTimings.shiftTimingsController import getShiftTimingsController,updateShiftTimingsController,currentShiftTimingController

shiftTimings_router=APIRouter()

@shiftTimings_router.get("/shift-timings",response_model=List[ShiftTimingResponse])
def getShiftTimingsRoute(db: Session = Depends(get_db)):
    return getShiftTimingsController(db)

@shiftTimings_router.put("/shift-timings",response_model=List[ShiftTimingResponse])
def updateShiftTimingsRoute(req:Request,shift_timings:List[ShiftTimingUpdate],db: Session = Depends(get_db)):
    return updateShiftTimingsController(req,db,shift_timings)

@shiftTimings_router.get("/current-shift",response_model=ShiftTimingResponse)
def currentShiftTimingRoute(db:Session=Depends(get_db)):
    return currentShiftTimingController(db)