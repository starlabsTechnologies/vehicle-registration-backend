from app.services.internalRfid.internalRfidServices import getVehicleReg,createVehicleReg,editVehicleReg,deleteVehicleReg,getAllotedTag,createAllotedTag
from app.models.vehicleRegistrationBase import FetchRfidResponse,VehicleRegistrationResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,SuccessResponse
from app.models.allotedTagsBase import ReceiptResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.services.internalRfid.internalRfidServices import getRfidFromServer

async def fetchVehicleRegControllerwithRfid(db:Session) -> FetchRfidResponse:
    try:
        rfid_data=await getRfidFromServer()
        vehicleReg=getVehicleReg(rfid_data['rfid'],db)

        if vehicleReg is None:
            logger.info(f"Fetched rfid tag: {rfid_data['rfid']}")
            return FetchRfidResponse(
                rfidTag=rfid_data['rfid']
            )
        
        else:        
            logger.info(f"Fetched vehicle reg with rfid tag: {rfid_data['rfid']}")
            return vehicleReg
    
    except Exception as error:
        logger.error(f"Error while fetching data: {error}")
        return JSONResponse(
            content={"message": "Error while fetching data"},
            status_code=500
        )

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