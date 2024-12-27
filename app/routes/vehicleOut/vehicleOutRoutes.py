from app.controllers.vehicleOut.vehicleOutController import fetchVehicleRegControllerwithRfid,getRfidFromServerController,openBarrierController
from fastapi import APIRouter,Depends
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from fastapi import Request,WebSocket,Body
from app.models.vehicleInOutBase import RfidTagModel

vehicleOut_router = APIRouter()

@vehicleOut_router.get("/vehicleOut-rfid-data")
async def increment_and_send_websocket(request:Request,db:Session=Depends(get_db)):
    return await fetchVehicleRegControllerwithRfid(request,db)

@vehicleOut_router.websocket('/vehicleOut-rfid-fetch')
async def fetch(websocket:WebSocket):
    await getRfidFromServerController(websocket)

@vehicleOut_router.post("/vehicleOut")
def openBarrierRequest(req:Request,rfidData: RfidTagModel,db:Session=Depends(get_db)):
    return openBarrierController(req,rfidData,db)