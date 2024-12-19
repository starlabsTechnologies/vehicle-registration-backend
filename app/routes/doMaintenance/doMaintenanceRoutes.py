from fastapi import APIRouter, Depends,Request
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.doMaintenanceBase import DONumberResponse,CreateDONumber,SuccessResponse,UpdateDONumber
from app.controllers.doMaintenance.doMaintenanceControllers import createDoNumberController,deleteDONumberController,getDoDataController,updateDONumberController

doMaintenance_router=APIRouter()

@doMaintenance_router.get('/do-maintenance/{doNumber}',response_model=DONumberResponse)
def getDoMaintenance(doNumber:str,db:Session=Depends(get_db)):
    return getDoDataController(doNumber,db)

@doMaintenance_router.post('/do-maintenance',response_model=SuccessResponse)
def createDoNumber(req:Request,doInfo:CreateDONumber,db:Session=Depends(get_db)):
    return createDoNumberController(req,doInfo,db)

@doMaintenance_router.delete('/do-maintenance/{doNumber}',response_model=SuccessResponse)
def deleteDoNumber(req:Request,doNumber:str,db:Session=Depends(get_db)):
    return deleteDONumberController(req,doNumber,db)

@doMaintenance_router.patch('/do-maintenance',response_model=SuccessResponse)
def updateDONumber(req:Request,doInfo:UpdateDONumber,db:Session=Depends(get_db)):
    return updateDONumberController(req,doInfo,db)

# {
#   "doNumber": "1212",
#   "weighbridgeNo":"2",
#   "transporter": "11",
#   "permissidoNameon": "",
#   "validThrough": "",
#   "validityTill": "2",
#   "allotedQty": 2.0,
#   "releasedQty": 2.0,
#   "leftQty": 0.0,
#   "doAddress": "",
#   "doRoute": "",
#   "salesOrder": "",
#   "customerId": "",
#   "mobileNumber": "1234567890"
# }

# {
#   "doNumber": "1212",
#   "weighbridgeNo": "1212",
#   "transporter": "1212",
#   "validityTill": "1212",
#   "allotedQty": 2.5,
#   "releasedQty": 3.0,
#   "doRoute": "1212",
#   "salesOrder": "1212",
#   "mobileNumber": "string"
# }