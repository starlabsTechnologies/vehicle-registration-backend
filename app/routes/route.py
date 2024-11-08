from fastapi import APIRouter
from app.routes.shiftTiming.shiftTimingRoutes import shiftTimings_router
from app.routes.auth.authRoute import auth_router
from app.routes.doMaintenance.doMaintenanceRoutes import doMaintenance_router

router = APIRouter()

@router.get('/')
async def route():
    return {"message": "Server Connection Established!"}

router.include_router(shiftTimings_router,prefix='/api')
router.include_router(auth_router,prefix='/api')
router.include_router(doMaintenance_router,prefix='/api')