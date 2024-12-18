from fastapi import APIRouter,Depends,WebSocket,Request
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.allotedTagsBase import ReceiptResponse
from app.models.vehicleRegistrationBase import FetchRfidResponse,VehicleRegistrationResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,SuccessResponse
from app.controllers.internalRfid.internalRfidControllers import getVehicleRegController,createVehicleRegController,editVehicleRegController,deleteVehicleRegController
from app.controllers.internalRfid.internalRfidControllers import getRfidFromServerController,fetchVehicleRegControllerwithRfid
from app.utils.webSocketManager.socketManager import WebSocketManager
from fastapi import WebSocket

vehicleReg_router=APIRouter()

@vehicleReg_router.get("/internal-rfid-data",response_model=FetchRfidResponse)
async def increment_and_send_websocket(request:Request,db:Session=Depends(get_db)):
    return await fetchVehicleRegControllerwithRfid(request,db)

@vehicleReg_router.websocket('/internal-rfid-fetch')
async def fetch(websocket:WebSocket):
    await getRfidFromServerController(websocket)

@vehicleReg_router.get('/internal-rfid/{rfidTag}',response_model=VehicleRegistrationResponse)
def getVehicleReg(rfidTag:str,db:Session=Depends(get_db)):
    return getVehicleRegController(rfidTag,db)

@vehicleReg_router.post('/internal-rfid',response_model=ReceiptResponse)
def createVehicleReg(req:Request,vehicleInfo:CreateVehicleRegistration,db:Session=Depends(get_db)):
    return createVehicleRegController(req,vehicleInfo,db)

@vehicleReg_router.put('/internal-rfid',response_model=SuccessResponse)
def editVehicleReg(req:Request,vehicleInfo:EditVehicleRegistration,db:Session=Depends(get_db)):
    return editVehicleRegController(req,vehicleInfo,db)

@vehicleReg_router.delete('/internal-rfid',response_model=SuccessResponse)
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