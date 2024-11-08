from fastapi import APIRouter, Depends
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.doMaintenanceBase import DONumberResponse,CreateDONumber,SuccessResponse
from app.controllers.doMaintenance.doMaintenanceControllers import createDoNumberController,deleteDONumberController,getDoDataController

doMaintenance_router=APIRouter()

@doMaintenance_router.get('/do-maintenance/{doNumber}',response_model=DONumberResponse)
def getDoMaintenance(doNumber:str,db:Session=Depends(get_db)):
    return getDoDataController(doNumber,db)

@doMaintenance_router.post('/do-maintenance',response_model=SuccessResponse)
def createDoNumber(doInfo:CreateDONumber,db:Session=Depends(get_db)):
    return createDoNumberController(doInfo,db)

@doMaintenance_router.delete('/do-maintenance/{doNumber}',response_model=SuccessResponse)
def deleteDoNumber(doNumber:str,db:Session=Depends(get_db)):
    return deleteDONumberController(doNumber,db)

# {
#   "doNumber": "1212",
#   "weighbridgeNo": "",
#   "transporter": "11",
#   "permissidoNameon": "",
#   "validThrough": "",
#   "validityTill": "",
#   "allotedQty": 0.0,
#   "releasedQty": 0.0,
#   "leftQty": 0.0,
#   "doAddress": "",
#   "doRoute": "",
#   "salesOrder": "",
#   "customerId": "",
#   "mobileNumber": "1234567890"
# }