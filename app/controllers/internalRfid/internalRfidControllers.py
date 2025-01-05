from app.services.internalRfid.internalRfidServices import getVehicleReg,createVehicleReg,editVehicleReg,deleteVehicleReg,getAllotedTag,createAllotedTag,createVehicleRegistrationLogs,createAllotedTagsLogs,editVehicleRegLogs,deleteVehicleRegLogs
from app.models.vehicleRegistrationBase import FetchRfidResponse,VehicleRegistrationResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,SuccessResponse
from app.models.allotedTagsBase import ReceiptResponse,NewAllotedReceiptResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import WebSocket, WebSocketDisconnect,Request
from app.utils.logger import logger
from app.utils.webSocketManager.socketManager import WebSocketManager
import asyncio
import json
from typing import Union

websocket_manager = WebSocketManager()

# trigger_event = asyncio.Event()
# rfid_data = None
# rfid_event = asyncio.Event()
# get_req_ip= None

connection_states = {}

async def getRfidFromServerController(websocket: WebSocket) -> None:
    # global rfid_data,get_req_ip
    # await websocket_manager.connect(websocket)

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

            # await trigger_event.wait()
            await state["trigger_event"].wait()

            # await websocket.send_text("trigger")
            # await websocket_manager.send_message("trigger",websocket)
            await websocket_manager.send_message("trigger", client_ip)
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")
            data_dict = json.loads(data)

            state["rfid_data"] = data_dict.get("rfid")
            if state["rfid_data"]:
                logger.info(f"Received RFID: {state['rfid_data']}")
                state["rfid_event"].set()

            # rfid_data = data_dict["rfid"]
            # if rfid_data:
            #     print(f"Received RFID: {rfid_data}")
            #     rfid_event.set()

            # trigger = False
            # await websocket.send_text("stop")
            # await websocket_manager.send_message("stop",websocket)
            # await websocket_manager.send_message("stop", get_req_ip)
            await websocket_manager.send_message("stop", client_ip)
            logger.info("Sent 'stop' to websocket")
            state["trigger_event"].clear()
            # trigger_event.clear()
            # await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        # await websocket_manager.disconnect(get_req_ip)
        if client_ip in connection_states:
            del connection_states[client_ip]

        await websocket_manager.disconnect(client_ip)

async def fetchVehicleRegControllerwithRfid(request:Request,db:Session) -> FetchRfidResponse:
    # trigger_event.set()
    # global rfid_data,get_req_ip
    # rfid_event.clear()

    # get_req_ip = request.client.host
    client_ip = request.client.host
    logger.info(f"Client IP in GET request: {client_ip}")

    if client_ip not in connection_states:
        return {"message": "No active WebSocket connection for this IP", "rfidTag": "00000000000000000000000"}
    
    state = connection_states[client_ip]

    state["trigger_event"].set()

    # websocket = websocket_manager.get_websocket(get_req_ip)

    # await rfid_event.wait()

    # if rfid_data is None:
    #     return {"message": "No RFID data received", "rfid": None}

    try:
        # Wait for RFID data or timeout
        await asyncio.wait_for(state["rfid_event"].wait(), timeout=10)
    except asyncio.TimeoutError:
        return {"message": "Timeout waiting for RFID data", "rfidTag": "00000000000000000000000"}

    rfid_data = state["rfid_data"]
    if not rfid_data:
        return {"message": "No RFID data received", "rfidTag": None}

    try:
        vehicleReg=getVehicleReg(rfid_data,db)
        tag=getAllotedTag(rfid_data,db)

        if tag is None:
            message="Not Alloted"
        else:
            message="Alloted"

        if vehicleReg is None:
            logger.info(f"Fetched rfid tag: {rfid_data}")
            return FetchRfidResponse(
                rfidTag=rfid_data,
                message=message
            )
        
        else:        
            logger.info(f"Fetched vehicle reg with rfid tag: {rfid_data}")
            vehicleReg.message = "Vehicle Registered successfully"
            return vehicleReg
    
    except Exception as error:
        logger.error(f"Error while fetching data: {error}")
        return JSONResponse(
            content={"message": "Error while fetching data"},
            status_code=500
        )

def getVehicleRegController(rfidTag: str, db: Session) -> VehicleRegistrationResponse:
    try:
        vehicleReg = getVehicleReg(rfidTag, db)

        if vehicleReg is None:
            logger.warning(f"Vehicle Registration for rfid tag {rfidTag} not found")
            return JSONResponse(
                content={"message": "Vehicle Registration not found."},
                status_code=404
            )
        
        # If message is "Vehicle not alloted", handle it specifically
        if vehicleReg.message == "Vehicle not alloted":
            logger.info(f"Vehicle with rfid tag {rfidTag} is not alloted")
            return JSONResponse(
                content={"message": vehicleReg.message},
                status_code=404  # or another status code if you prefer
            )
        
        logger.info(f"Fetched vehicle reg with rfid tag: {rfidTag}")
        return vehicleReg
    
    except Exception as error:
        logger.error(f"Error while fetching data: {error}")
        return JSONResponse(
            content={"message": "Error while fetching data"},
            status_code=500
        )

def createVehicleRegController(req:Request,vehicleInfo:CreateVehicleRegistration,db:Session) -> Union[ReceiptResponse,NewAllotedReceiptResponse]:
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

        if not vehicleInfo.rfidTag:
            logger.warning("Rfid tag required")
            return JSONResponse(
                content={"message":"Rfid Tag required"},
                status_code=400
            )
        
        if not vehicleInfo.vehicleNumber or not vehicleInfo.validityTill:
            logger.warning("Vehicle Number and ValidityTill required")
            return JSONResponse(
                content={"message":"Vehicle Number and ValidityTill required"},
                status_code=400
            )
        
        if not vehicleInfo.total:
            logger.warning("Total value required")
            return JSONResponse(
                content={"message":"Total value required"},
                status_code=400
            )

        vehicleReg=getVehicleReg(vehicleInfo.rfidTag,db)

        if vehicleReg is not None:
            logger.warning(f"Vehicle with Rfid Tag {vehicleInfo.rfidTag} already exists")
            return JSONResponse(
                content={"message": "Vehicle with Rfid Tag already exists"},
                status_code=400
            )
        
        tag=getAllotedTag(vehicleInfo.rfidTag,db)

        if tag is None:
            newTag=createAllotedTag(vehicleInfo,db)

            if newTag:
                createLog = createAllotedTagsLogs(vehicleInfo,db,actionByUsername)
                if(createLog):
                    logger.info("Alloted Tag create logged successfully")
                else:
                    logger.info("Logging of Alloted Tag creation unsuccessful")

                newReg=createVehicleReg(vehicleInfo,db)

                if not newReg:
                    logger.warning("Error occurred registering vehicle")
                    return JSONResponse(
                        content={"message":"Error occurred while registering vehicle"},
                        status_code=400
                    )
                
                logger.info(f"Vehicle Registered successfully")

                createVehicleRegLog = createVehicleRegistrationLogs(vehicleInfo,db,actionByUsername)
                if(createVehicleRegLog):
                    logger.info("Vehicle registration logged successfully")
                else:
                    logger.info("Logging of Vehicle registration unsuccessful")

                newTag.message = "Vehicle Registered successfully"
                return newTag
        
            else:
                logger.warning("Error occurred while Alloting Tag")
                return JSONResponse(
                    content={"message":"Error occurred while Alloting Tag"},
                    status_code=400
                )
        
        newReg=createVehicleReg(vehicleInfo,db)

        if not newReg:
            logger.warning("Error occurred registering vehicle")
            return JSONResponse(
                content={"message":"Error occurred while registering vehicle"},
                status_code=400
            )
        
        logger.info(f"Vehicle Registered successfully")

        createVehicleRegLog = createVehicleRegistrationLogs(vehicleInfo,db,actionByUsername)
        if(createVehicleRegLog):
            logger.info("Vehicle registration logged successfully")
        else:
            logger.info("Logging of Vehicle registration unsuccessful")

        return ReceiptResponse(
            rfidTag=tag.rfidTag,
            typeOfVehicle=tag.typeOfVehicle,
            vehicleNumber=tag.vehicleNumber,
            regDate=tag.regDate,
            regTime=tag.regTime,
            userid=tag.userid,
            barrierGate=tag.barrierGate,
            salesType=tag.salesType,
            due=tag.due,
            message="Vehicle Registered successfully"
        )
    
    except Exception as error:
        logger.error(f"Error occurred while registering vehicle: {error}")
        return JSONResponse(
            content={"message": "Error occurred while registering vehicle"},
            status_code=500
        )

def editVehicleRegController(req:Request,vehicleInfo:EditVehicleRegistration,db:Session) -> SuccessResponse:
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

        if not vehicleInfo.rfidTag:
            logger.warning("Rfid tag required")
            return JSONResponse(
                content={"message":"Rfid Tag required"},
                status_code=400
            )
        
        if not vehicleInfo.vehicleNumber or not vehicleInfo.validityTill:
            logger.warning("Vehicle Number and ValidityTill required")
            return JSONResponse(
                content={"message":"Vehicle Number and ValidityTill required"},
                status_code=400
            )
        
        edited=editVehicleReg(vehicleInfo,db)

        if edited is None:
            logger.warning(f"Vehicle Registration for rfid tag {vehicleInfo.rfidTag} not found")
            return JSONResponse(
                content={"message":"Vehicle Registration not found."},
                status_code=404
            )
        
        logger.info(f"Vehicle Registration updated successfully")

        editLog = editVehicleRegLogs(vehicleInfo,db,actionByUsername)
        if(editLog):
            logger.info("Vehicle registration edit logged successfully")
        else:
            logger.info("Logging of Vehicle registration edit unsuccessful")

        return SuccessResponse(
            message="Vehicle Registration updated successfully"
        )
    
    except Exception as error:
        logger.error(f"Error occurred while updating data: {error}")
        return JSONResponse(
            content={"message": "Error updating data"},
            status_code=500
        )

def deleteVehicleRegController(req:Request,vehicleInfo:DeleteVehicleRegistration,db:Session) -> SuccessResponse:
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

        if not vehicleInfo.rfidTag:
            logger.warning("Rfid tag required")
            return JSONResponse(
                content={"message":"Rfid Tag required"},
                status_code=400
            )
        
        success=deleteVehicleReg(vehicleInfo,db)

        if success is None:
            logger.warning(f"Vehicle Registration for rfid tag {vehicleInfo.rfidTag} not found")
            return JSONResponse(
                content={"message":"Vehicle Registration not found."},
                status_code=404
            )
        
        if not success:
            logger.warning("Error deleting data")
            return JSONResponse(
                content={"message": "Error deleting data"},
                status_code=400
            )
        
        logger.info(f"Vehicle deleted successfully")

        delLog = deleteVehicleRegLogs(vehicleInfo,db,actionByUsername)
        if(delLog):
            logger.info("Vehicle registration deletion logged successfully")
        else:
            logger.info("Logging of Vehicle registration deletion unsuccessful")

        return SuccessResponse(
            message="Data has been deleted successfully"
        )
    
    except Exception as error:
        logger.error(f"Error occurred while deleting data: {error}")
        return JSONResponse(
            content={"message": "Error deleting data"},
            status_code=500
        )