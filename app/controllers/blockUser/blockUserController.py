# from app.services.blockUser.blockUserServices import changeBlacklistStatus,getRfidFromServer
from fastapi import HTTPException, requests
from app.services.blockUser.blockUserServices import changeBlacklistStatus
from app.models.allotedTagsBase import BlockUser,SuccessResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.utils.logger import logger

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