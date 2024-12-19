from app.services.externalRfid.externalRfidServices import getVehicleReg,createVehicleReg,editVehicleReg,deleteVehicleReg,getAllotedTag,createVehicleRegistrationLogs,editVehicleRegLogs,deleteVehicleRegLogs
from app.models.vehicleRegistrationBase import VehicleRegistrationResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,SuccessResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.models.allotedTagsBase import ReceiptResponse
from app.utils.logger import logger
from fastapi import Request

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

def createVehicleRegController(req:Request,vehicleInfo:CreateVehicleRegistration,db:Session) -> ReceiptResponse:
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

        vehicleReg=getVehicleReg(vehicleInfo.rfidTag,db)

        if vehicleReg is not None:
            logger.warning(f"Vehicle with Rfid Tag {vehicleInfo.rfidTag} already exists")
            return JSONResponse(
                content={"message": "Vehicle with Rfid Tag already exists"},
                status_code=400
            )
        
        tag=getAllotedTag(vehicleInfo.rfidTag,db)
        
        if tag is None:
            logger.warning(f"Vehicle with Rfid Tag {vehicleInfo.rfidTag} not alloted tag")
            return JSONResponse(
                content={"message": f"Vehicle with Rfid Tag {vehicleInfo.rfidTag} not alloted tag"},
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