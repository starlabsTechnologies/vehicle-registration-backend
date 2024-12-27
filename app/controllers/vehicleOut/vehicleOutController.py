from app.utils.logger import logger
from app.utils.webSocketManager.socketManager import WebSocketManager
from app.models.vehicleInOutBase import FetchRfidResponseVehicleOut,RfidTagModel
from app.services.vehicleOut.vehicleOutServices import getVehicleOut,openBarrier,updateVehicleInOutLogs
from fastapi import WebSocket, WebSocketDisconnect,Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import asyncio
import json

websocket_manager = WebSocketManager()

connection_states = {}

async def getRfidFromServerController(websocket: WebSocket) -> None:
    client_ip = websocket.client.host
    logger.info(f"Client connected: {client_ip}")
    await websocket_manager.connect(websocket, client_ip) 

    if client_ip not in connection_states:
        connection_states[client_ip] = {
            "websocket": websocket,
            "trigger_event": asyncio.Event(),
            "rfid_event": asyncio.Event(),
            "rfid_data": None,
        }

    try:
        while True:
            state = connection_states[client_ip]

            await state["trigger_event"].wait()
            await websocket_manager.send_message("trigger_vehicleOut", client_ip)
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")
            data_dict = json.loads(data)

            state["rfid_data"] = data_dict.get("rfid")
            if state["rfid_data"]:
                logger.info(f"Received RFID: {state['rfid_data']}")
                state["rfid_event"].set()

            await websocket_manager.send_message("stop_vehicleOut", client_ip)
            logger.info("Sent 'stop' to websocket")
            state["trigger_event"].clear()

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        if client_ip in connection_states:
            del connection_states[client_ip]

        await websocket_manager.disconnect(client_ip)

async def fetchVehicleRegControllerwithRfid(request:Request,db:Session) -> FetchRfidResponseVehicleOut:
    client_ip = request.client.host
    logger.info(f"Client IP in GET request: {client_ip}")

    if client_ip not in connection_states:
        return {"message": "No active WebSocket connection for this IP", "rfidTag": "00000000000000000000000"}
    
    state = connection_states[client_ip]

    state["trigger_event"].set()

    try:
        await asyncio.wait_for(state["rfid_event"].wait(), timeout=10)
    except asyncio.TimeoutError:
        return {"message": "Timeout waiting for RFID data", "rfidTag": "00000000000000000000000"}

    rfid_data = state["rfid_data"]
    if not rfid_data:
        return {"message": "No RFID data received", "rfidTag": None}

    try:
        vehicleIn=getVehicleOut(rfid_data,db)

        if vehicleIn is None:
            logger.info(f"Fetched rfid tag: {rfid_data}")
            return FetchRfidResponseVehicleOut(
                rfidTag=rfid_data,
                status="Vehicle Not Registered"
            )
        
        else:        
            logger.info(f"Fetched vehicle reg with rfid tag: {rfid_data}")
            return vehicleIn
    
    except Exception as error:
        logger.error(f"Error while fetching data: {error}")
        return JSONResponse(
            content={"message": "Error while fetching data"},
            status_code=500
        )
    
def openBarrierController(req:Request,rfidData:RfidTagModel,db:Session):
    try:
        headers = req.headers
        authorization = headers.get("authorization")
        if not authorization:
            logger.warning("Authorization header missing")
            return JSONResponse(
                content={"message": "Authorization header missing"},
                status_code=400
            )
        
        actionByUsername = authorization

        success=openBarrier(rfidData.rfidTag,db)

        if success is None:
            logger.warning(f"Vehicle with rfidTag: {rfidData.rfidTag} not found")
            return JSONResponse(
                content={"message": f"Vehicle with rfidTag: {rfidData.rfidTag} not found"},
                status_code=404
            )
        
        logger.info("Barrier Opened Successfully")
        updateLogs=updateVehicleInOutLogs(rfidData.rfidTag,db,actionByUsername)
        if(updateLogs):
            logger.info("Vehicle In Out edit logged successfully")
        else:
            logger.info("Logging of Vehicle In Out edit unsuccessful")
        return JSONResponse(
            content={"message":"Barrier Opened Successfully"},
            status_code=200
        )

    except Exception as error:
        logger.error(f"Error occured while opening barrier: {error}")
        return JSONResponse(
            content={"message": "Error occured while opening barrier"},
            status_code=500
        )