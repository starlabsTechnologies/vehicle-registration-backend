# from app.services.blockUser.blockUserServices import changeBlacklistStatus,getRfidFromServer
from app.services.blockUser.blockUserServices import changeBlacklistStatus
from app.models.allotedTagsBase import BlockUser,SuccessResponse,ServiceResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.utils.logger import logger
import httpx
from app.utils.rfidData.rfidData import rfid_data

async def fetchRfidTagController(request_data):
    try:
        rfid_data["rfid"] = request_data.get("rfid")
        rfid_data["success"] = request_data.get("success")
        logger.info("Rfid Tag fetched from exe file")
        return rfid_data
    except Exception as error:
        logger.error(f"Error occurred while fetching rfid Tag from exe file: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching rfid Tag from exe file"},
            status_code=500
        )

async def getRfidDataController():
    try:
        if not rfid_data:
            await triggerPostRequestController()
        logger.info("Rfid Tag fetched from global file")
        return rfid_data
    except Exception as error:
        logger.error(f"Error occurred while fetching rfid Tag from global file: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching rfid Tag from global file"},
            status_code=500
        )

async def triggerPostRequestController():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8000/rfid-connect", json={"rfid": "sample_rfid", "success": True})
            if response.status_code == 200:
                data = response.json()
                rfid_data["rfid"] = data.get("rfid")
                rfid_data["success"] = data.get("success")
                logger.info(f"Data from POST request: {rfid_data}")
            else:
                logger.warning("Failed to fetch RFID data from POST request")
    except Exception as error:
        logger.error(f"Error during POST request: {error}")
        return JSONResponse(
            content={"message": "Error during POST request"},
            status_code=500
        )

def blockUserController(userInfo:BlockUser,db:Session) -> SuccessResponse:
    try:
        user=changeBlacklistStatus(userInfo.rfidTag,userInfo.vehicleNo,userInfo.action,db)

        if user is None:
            logger.warning(f"User not found: {userInfo.rfidTag}")
            return JSONResponse(
                content={"message":"User Not Found","isBlocked":False},
                status_code=404
            )
        
        if user is False:
            logger.warning(f"User is already {userInfo.action}.")
            return JSONResponse(
                content={"message":f"User is already {userInfo.action}.","isBlocked":False},
                status_code=400
            )
        
        logger.info("User status updated successfully.")
        return SuccessResponse(
            message="User status updated successfully.",
            isBlocked=True
        )
    
    except Exception as error:
        logger.error(f"Error occurred while blocking user: {error}")
        return JSONResponse(
            content={"message": "Error occurred while blocking user"},
            status_code=500
        )


# 52b337794fc6143f