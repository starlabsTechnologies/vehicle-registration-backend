from sqlalchemy.orm import Session
from app.services.auth.authServices import getUserByUserName
from app.models.userInfoBase import UserInfoResponse,EditUser,SuccessResponse
from fastapi.responses import JSONResponse
from app.services.changePass.changePassServices import editUser

def getUserController(username:str,db:Session) -> UserInfoResponse:
    user=getUserByUserName(username,db)

    if user is None:
        return JSONResponse(
            content={"message": "User doesnt exist"},
            status_code=404
        )
    
    return user

def editUserController(userInfo:EditUser,db:Session) -> SuccessResponse:
    if(len(userInfo.mobileNumber)!=10 and len(userInfo.mobileNumber)!=0):
        return JSONResponse(
            content={"message": "Mobile Number should be 10 digits exactly!"},
            status_code=400
        )

    edited=editUser(userInfo,db)

    if edited is None:
        return JSONResponse(
            content={"message": "User Not Found"},
            status_code=404
        )
    
    return SuccessResponse(message="User details saved successfully")