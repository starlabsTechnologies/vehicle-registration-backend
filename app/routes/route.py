from fastapi import APIRouter
from app.routes.shiftTiming.shiftTimingRoutes import shiftTimings_router
from app.routes.auth.authRoute import auth_router
from app.routes.doMaintenance.doMaintenanceRoutes import doMaintenance_router
from app.routes.blockUser.blockUserRoutes import blockUser_router
from app.routes.changePass.changePassRoutes import changePass_router
from app.routes.internalRfid.internalRfidRoutes import vehicleReg_router
from app.routes.externalRfid.externalRfidRoutes import externalrfid_Router
from app.routes.report.reportRoutes import report_router

router = APIRouter()

@router.get('/')
async def route():
    return {"message": "Server Connection Established!"}

router.include_router(shiftTimings_router,prefix='/api')
router.include_router(auth_router,prefix='/api')
router.include_router(doMaintenance_router,prefix='/api')
router.include_router(blockUser_router,prefix='/api')
router.include_router(changePass_router,prefix='/api')
router.include_router(vehicleReg_router,prefix='/api')

router.include_router(externalrfid_Router,prefix='/api')

router.include_router(report_router,prefix='/api')