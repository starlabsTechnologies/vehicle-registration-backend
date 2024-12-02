from app.services.blockUser.blockUserServices import changeBlacklistStatus,getRfidFromServer
from app.models.allotedTagsBase import BlockUser,SuccessResponse,ServiceResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.utils.logger import logger
import httpx

async def getRfidFromServiceController() -> ServiceResponse:
    try:
        response=await getRfidFromServer()

        if not response.success:
            logger.warning("Tag not found")
            return JSONResponse(
                content={"message": "Tag not found"},
                status_code=400
            )
        
        logger.info("Rfid Tag fetched successfully.")
        return response

    except Exception as error:
        logger.error(f"Error occured while fetching Rfid: {error}")
        return JSONResponse(
            content={"message": f"Error occured while fetching Rfid: {error}"},
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