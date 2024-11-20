from fastapi import APIRouter,Depends
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.vehicleRegistrationBase import RegistrationDetailsResponse
from app.controllers.report.reportControllers import getSummaryController,setOptionController
from app.models.vehicleInOutBase import VehicleInOutResponse,DataFilter
from typing import List,Union

report_router=APIRouter()

@report_router.post('/report',response_model=List[Union[VehicleInOutResponse, RegistrationDetailsResponse]])
def setOption(filterInfo:DataFilter,db:Session=Depends(get_db)):
    return setOptionController(filterInfo,db)

# {
#   "dateIn": "2024-09-11",
#   "dateOut": "2024-09-12",
#   "timeIn": "03:33",
#   "timeOut": "15:33"
# }