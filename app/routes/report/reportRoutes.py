from fastapi import APIRouter,Depends,Query
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.vehicleRegistrationBase import RegistrationDetailsResponse
from app.controllers.report.reportControllers import setOptionController,getRegistrationDetailsController,getVehicleInOutDataController
from app.models.vehicleInOutBase import VehicleInOutResponse,DataFilter,OptionsEnum
from typing import List,Union,Optional

report_router=APIRouter()

@report_router.get('/report',response_model=List[VehicleInOutResponse])
def setOption(db:Session=Depends(get_db),option: OptionsEnum = Query(None),dateIn: Optional[str] = Query(None),dateOut: Optional[str] = Query(None),timeIn: Optional[str] = Query(None),timeOut: Optional[str] = Query(None)):
    return setOptionController(db,option,dateIn,dateOut,timeIn,timeOut)

@report_router.get('/report',response_model=List[VehicleInOutResponse])
def getVehicleInOut(db:Session=Depends(get_db)):
    return getVehicleInOutDataController(db)

@report_router.get('/report/registration-details',response_model=List[RegistrationDetailsResponse])
def getRegistrationDetails(db:Session=Depends(get_db)):
    return getRegistrationDetailsController(db)

# {
#   "dateIn": "2024-09-11",
#   "dateOut": "2024-09-12",
#   "timeIn": "03:33",
#   "timeOut": "15:33"
# }