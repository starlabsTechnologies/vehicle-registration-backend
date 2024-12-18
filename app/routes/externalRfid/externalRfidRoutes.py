from fastapi import APIRouter,Depends
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from fastapi import Request
from app.models.allotedTagsBase import ReceiptResponse
from app.models.vehicleRegistrationBase import VehicleRegistrationResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,SuccessResponse
from app.controllers.externalRfid.externalRfidController import getVehicleRegController,createVehicleRegController,editVehicleRegController,deleteVehicleRegController

externalrfid_Router=APIRouter()

@externalrfid_Router.get('/external-rfid/{rfidTag}',response_model=VehicleRegistrationResponse)
def getVehicleReg(rfidTag:str,db:Session=Depends(get_db)):
    return getVehicleRegController(rfidTag,db)

@externalrfid_Router.post('/external-rfid',response_model=ReceiptResponse)
def createVehicleReg(req:Request,vehicleInfo:CreateVehicleRegistration,db:Session=Depends(get_db)):
    return createVehicleRegController(req,vehicleInfo,db)

@externalrfid_Router.put('/external-rfid',response_model=SuccessResponse)
def editVehicleReg(req:Request,vehicleInfo:EditVehicleRegistration,db:Session=Depends(get_db)):
    return editVehicleRegController(req,vehicleInfo,db)

@externalrfid_Router.delete('/external-rfid',response_model=SuccessResponse)
def deleteVehicleReg(req:Request,vehicleInfo:DeleteVehicleRegistration,db:Session=Depends(get_db)):
    return deleteVehicleRegController(req,vehicleInfo,db)


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