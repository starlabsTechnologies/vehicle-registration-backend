from fastapi import APIRouter,Depends
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.vehicleRegistrationBase import VehicleRegistrationResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,SuccessResponse
from app.controllers.externalRfid.externalRfidController import getVehicleRegController,createVehicleRegController,editVehicleRegController,deleteVehicleRegController

externalrfid_Router=APIRouter()

@externalrfid_Router.get('/external-rfid/{rfidTag}',response_model=VehicleRegistrationResponse)
def getVehicleReg(rfidTag:str,db:Session=Depends(get_db)):
    return getVehicleRegController(rfidTag,db)

@externalrfid_Router.post('/external-rfid',response_model=SuccessResponse)
def createVehicleReg(vehicleInfo:CreateVehicleRegistration,db:Session=Depends(get_db)):
    return createVehicleRegController(vehicleInfo,db)

@externalrfid_Router.put('/external-rfid',response_model=SuccessResponse)
def editVehicleReg(vehicleInfo:EditVehicleRegistration,db:Session=Depends(get_db)):
    return editVehicleRegController(vehicleInfo,db)

@externalrfid_Router.delete('/external-rfid',response_model=SuccessResponse)
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