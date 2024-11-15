from app.services.blockUser.blockUserServices import authorizeUser,AuthResult,changeBlacklistStatus
from app.models.allotedTagsBase import AuthorizeUser,BlockUser,SuccessResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

def authorizeUserController(userInfo:AuthorizeUser,db:Session) -> SuccessResponse:
    user=authorizeUser(userInfo.username,userInfo.password,db)

    if user is AuthResult.USER_NOT_FOUND:
        return JSONResponse(
            content={"message":"User Not Found","isAuthorized":False},
            status_code=404
        )
    
    if user is AuthResult.INCORRECT_PASSWORD:
        return JSONResponse(
            content={"message":"Incorrect Password","isAuthorized":False},
            status_code=401
        )
    
    if user is AuthResult.UNAUTHORIZED_ACCESS:
        return JSONResponse(
            content={"message":"User is not authorized to change credentials.","isAuthorized":False},
            status_code=403
        )
    
    return SuccessResponse(
        message="User is Authorized",
        isAuthorized=True
    )

def blockUserController(userInfo:BlockUser,db:Session) -> SuccessResponse:
    user=changeBlacklistStatus(userInfo.rfidTag,userInfo.vehicleNo,userInfo.action,db)

    if user is None:
        return JSONResponse(
            content={"message":"User Not Found","isBlocked":False},
            status_code=404
        )
    
    if user is False: 
        return JSONResponse(
            content={"message":f"User is already {userInfo.action}.","isBlocked":False},
            status_code=400
        )
    
    return SuccessResponse(
        message="User status updated successfully.",
        isBlocked=True
    ) 


# 52b337794fc6143f