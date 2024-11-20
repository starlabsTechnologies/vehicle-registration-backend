from fastapi import APIRouter,Depends
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.vehicleRegistrationBase import VehicleRegistrationResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,SuccessResponse
from app.controllers.internalRfid.internalRfidControllers import getVehicleRegController,createVehicleRegController,editVehicleRegController,deleteVehicleRegController

vehicleReg_router=APIRouter()

@vehicleReg_router.get('/internal-rfid/{rfidTag}',response_model=VehicleRegistrationResponse)
def getVehicleReg(rfidTag:str,db:Session=Depends(get_db)):
    return getVehicleRegController(rfidTag,db)

@vehicleReg_router.post('/internal-rfid',response_model=SuccessResponse)
def createVehicleReg(vehicleInfo:CreateVehicleRegistration,db:Session=Depends(get_db)):
    return createVehicleRegController(vehicleInfo,db)

@vehicleReg_router.put('/internal-rfid',response_model=SuccessResponse)
def editVehicleReg(vehicleInfo:EditVehicleRegistration,db:Session=Depends(get_db)):
    return editVehicleRegController(vehicleInfo,db)

@vehicleReg_router.delete('/internal-rfid',response_model=SuccessResponse)
def deleteVehicleReg(vehicleInfo:DeleteVehicleRegistration,db:Session=Depends(get_db)):
    return deleteVehicleRegController(vehicleInfo,db)


# {
#   "rfidTag": "jidd",
#   "typeOfVehicle": "TCT",
#   "vehicleNumber": "",
#   "doNumber": "",
#   "transporter": "",
#   "driverOwner": "",
#   "weighbridgeNo": "",
#   "visitPurpose": "",
#   "placeToVisit": "",
#   "personToVisit": "",
#   "validityTill": "",
#   "section": "",
#   "registerDate": "",
#   "registerTime": ""
# }