from fastapi import APIRouter,Depends,WebSocket
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.allotedTagsBase import ReceiptResponse
from app.models.vehicleRegistrationBase import FetchRfidResponse,VehicleRegistrationResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,SuccessResponse
from app.controllers.internalRfid.internalRfidControllers import getVehicleRegController,createVehicleRegController,editVehicleRegController,deleteVehicleRegController
from app.controllers.internalRfid.internalRfidControllers import getRfidFromServerController,fetchVehicleRegControllerwithRfid
from app.utils.webSocketManager.socketManager import WebSocketManager
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json

vehicleReg_router=APIRouter()

# websocket_manager = WebSocketManager()

# trigger_event = asyncio.Event()
# rfid_data=None

# async def getRfidFromServer(websocket: WebSocket,db:Session) -> None:
#     global rfid_data
#     await websocket_manager.connect(websocket)
#     global trigger
#     try:
#         while True:
#             await trigger_event.wait()

#             await websocket.send_text("trigger")
#             data = await websocket.receive_text()
#             print(f"Received message: {data}")
#             data_dict = json.loads(data)

#             rfid_data = data_dict["rfid"]  # Extract RFID tag from the message

#             trigger = False
#             await websocket.send_text("stop")
#             print("Sent 'stop' to websocket")
#             trigger_event.clear()
#             await asyncio.sleep(0.5)
        
#     except WebSocketDisconnect:
#         print("WebSocket disconnected")

@vehicleReg_router.get("/internal-rfid-data",response_model=FetchRfidResponse)
async def increment_and_send_websocket(db:Session=Depends(get_db)):
    return await fetchVehicleRegControllerwithRfid(db)

@vehicleReg_router.websocket('/internal-rfid-fetch')
async def fetch(websocket:WebSocket):
    await getRfidFromServerController(websocket)

@vehicleReg_router.get('/internal-rfid/{rfidTag}',response_model=VehicleRegistrationResponse)
def getVehicleReg(rfidTag:str,db:Session=Depends(get_db)):
    return getVehicleRegController(rfidTag,db)

@vehicleReg_router.post('/internal-rfid',response_model=ReceiptResponse)
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