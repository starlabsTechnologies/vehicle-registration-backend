from fastapi import APIRouter
from app.routes.shiftTiming.shiftTimingRoutes import shiftTimings_router

router = APIRouter()

@router.get('/')
async def route():
    return {"message": "Server Connection Established!"}

router.include_router(shiftTimings_router,prefix='/api')