from app.services.internalRfid.internalRfidServices import getVehicleReg,createVehicleReg,editVehicleReg,deleteVehicleReg,getAllotedTag,createAllotedTag
from app.models.vehicleRegistrationBase import FetchRfidResponse,VehicleRegistrationResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,SuccessResponse
from app.models.allotedTagsBase import ReceiptResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import WebSocket, WebSocketDisconnect
from app.utils.logger import logger
from app.utils.webSocketManager.socketManager import WebSocketManager
import asyncio
import json

websocket_manager = WebSocketManager()

trigger_event = asyncio.Event()
rfid_data = None
rfid_event = asyncio.Event()

async def getRfidFromServerController(websocket: WebSocket) -> None:
    global rfid_data
    await websocket_manager.connect(websocket)
    global trigger
    try:
        while True:
            await trigger_event.wait()

            await websocket.send_text("trigger")
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            data_dict = json.loads(data)

            rfid_data = data_dict["rfid"]
            if rfid_data:
                print(f"Received RFID: {rfid_data}")
                rfid_event.set() 

            trigger = False
            await websocket.send_text("stop")
            print("Sent 'stop' to websocket")
            trigger_event.clear()
            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        print("WebSocket disconnected")

async def fetchVehicleRegControllerwithRfid(db:Session) -> FetchRfidResponse:
    trigger_event.set()
    global rfid_data
    rfid_event.clear()

    await rfid_event.wait()

    if rfid_data is None:
        return {"message": "No RFID data received", "rfid": None}

    try:
        vehicleReg=getVehicleReg(rfid_data,db)

        if vehicleReg is None:
            logger.info(f"Fetched rfid tag: {rfid_data}")
            return FetchRfidResponse(
                rfidTag=rfid_data
            )
        
        else:        
            logger.info(f"Fetched vehicle reg with rfid tag: {rfid_data}")
            return vehicleReg
    
    except Exception as error:
        logger.error(f"Error while fetching data: {error}")
        return JSONResponse(
            content={"message": "Error while fetching data"},
            status_code=500
        )

# async def fetchVehicleRegControllerwithRfid(db:Session) -> FetchRfidResponse:
#     try:
#         vehicleReg=getVehicleReg(rfid_data['rfid'],db)

#         if vehicleReg is None:
#             logger.info(f"Fetched rfid tag: {rfid_data['rfid']}")
#             return FetchRfidResponse(
#                 rfidTag=rfid_data['rfid']
#             )
        
#         else:        
#             logger.info(f"Fetched vehicle reg with rfid tag: {rfid_data['rfid']}")
#             return vehicleReg
    
#     except Exception as error:
#         logger.error(f"Error while fetching data: {error}")
#         return JSONResponse(
#             content={"message": "Error while fetching data"},
#             status_code=500
#         )

def getVehicleRegController(rfidTag:str,db:Session) -> VehicleRegistrationResponse:
    try:
        vehicleReg=getVehicleReg(rfidTag,db)

        if vehicleReg is None:
            logger.warning(f"Vehicle Registration for rfid tag {rfidTag} not found")
            return JSONResponse(
                content={"message":"Vehicle Registration not found."},
                status_code=404
            )
        
        logger.info(f"Fetched vehicle reg with rfid tag: {rfidTag}")
        return vehicleReg
    
    except Exception as error:
        logger.error(f"Error while fetching data: {error}")
        return JSONResponse(
            content={"message": "Error while fetching data"},
            status_code=500
        )

def createVehicleRegController(vehicleInfo:CreateVehicleRegistration,db:Session) -> ReceiptResponse:
    try:
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
                newReg=createVehicleReg(vehicleInfo,db)

                if not newReg:
                    logger.warning("Error occurred registering vehicle")
                    return JSONResponse(
                        content={"message":"Error occurred while registering vehicle"},
                        status_code=400
                    )
                
                logger.info(f"Vehicle Registered successfully")
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
        tag.message = "Vehicle Registered successfully"
        return tag
    
    except Exception as error:
        logger.error(f"Error occurred while registering vehicle: {error}")
        return JSONResponse(
            content={"message": "Error occurred while registering vehicle"},
            status_code=500
        )

def editVehicleRegController(vehicleInfo:EditVehicleRegistration,db:Session) -> SuccessResponse:
    try:
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
        return SuccessResponse(
            message="Vehicle Registration updated successfully"
        )
    
    except Exception as error:
        logger.error(f"Error occurred while updating data: {error}")
        return JSONResponse(
            content={"message": "Error updating data"},
            status_code=500
        )

def deleteVehicleRegController(vehicleInfo:DeleteVehicleRegistration,db:Session) -> SuccessResponse:
    try:
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
        return SuccessResponse(
            message="Data has been deleted successfully"
        )
    
    except Exception as error:
        logger.error(f"Error occurred while deleting data: {error}")
        return JSONResponse(
            content={"message": "Error deleting data"},
            status_code=500
        )