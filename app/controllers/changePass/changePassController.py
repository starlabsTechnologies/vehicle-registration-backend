from sqlalchemy.orm import Session
from app.services.auth.authServices import getUserByUserName
from app.models.userInfoBase import UserInfoResponse,EditUser,SuccessResponse
from fastapi.responses import JSONResponse
from app.services.changePass.changePassServices import editUser,changePassLogs
from app.utils.logger import logger
from fastapi import Request

def getUserController(username:str,db:Session) -> UserInfoResponse:
    try:
        user=getUserByUserName(username,db)

        if user is None:
            logger.warning("User doesnt exist")
            return JSONResponse(
                content={"message": "User doesnt exist"},
                status_code=404
            )
        
        logger.info(f"Fetched user with username: {username}")
        return user
    
    except Exception as error:
        logger.error(f"Error occurred while fetching user: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching user"},
            status_code=500
        )

def editUserController(req:Request,userInfo:EditUser,db:Session) -> SuccessResponse:
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

        if(len(userInfo.mobileNumber)!=10 and len(userInfo.mobileNumber)!=0):
            logger.warning("Mobile Number should be 10 digits exactly!")
            return JSONResponse(
                content={"message": "Mobile Number should be 10 digits exactly!"},
                status_code=400
            )

        edited=editUser(userInfo,db)

        if edited is None:
            logger.warning(f"User {userInfo.username} Not Found")
            return JSONResponse(
                content={"message": "User Not Found"},
                status_code=404
            )
        
        logger.info("User details saved successfully")

        logChangePass = changePassLogs(userInfo.username,db,actionByUsername)
        if(logChangePass):
            logger.info("User edit logged successfully")
        else:
            logger.info("Logging of User edit log unsuccessful")
        return SuccessResponse(message="User details saved successfully")
    
    except Exception as error:
        logger.error(f"Error occurred while editing user details: {error}")
        return JSONResponse(
            content={"message": "Error occurred while editing user details"},
            status_code=500
        )