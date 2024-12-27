from app.controllers.vehicleIn.vehicleInController import fetchVehicleRegControllerwithRfid,getRfidFromServerController
from fastapi import APIRouter,Depends
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from fastapi import Request,WebSocket

vehicleIn_router = APIRouter()

@vehicleIn_router.post("/vehicleIn-rfid-data")
async def increment_and_send_websocket(request:Request,db:Session=Depends(get_db)):
    return await fetchVehicleRegControllerwithRfid(request,db)

@vehicleIn_router.websocket('/vehicleIn-rfid-fetch')
async def fetch(websocket:WebSocket):
    await getRfidFromServerController(websocket)