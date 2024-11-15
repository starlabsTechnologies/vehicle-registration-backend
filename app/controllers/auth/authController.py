from app.services.auth.authServices import getUserByUserName,logUserIn, createUser,deleteUserByUsername
from app.models.userInfoBase import UserInfoResponse,UserLogin,CreateUser
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

def logUserInController(userInfo:UserLogin,db:Session) -> UserInfoResponse:
    user=logUserIn(userInfo.username,userInfo.password,db)

    if user is None:
        return JSONResponse(
            content={"message": "User Not Found"},
            status_code=404
        )
    
    if user is False:
        return JSONResponse(
            content={"message": "Incorrect Password"},
            status_code=401
        )
    
    user.message = "User logged in"
    return user

def createUserController(userInfo: CreateUser,db:Session) -> JSONResponse:
    if((not userInfo.password) or (not userInfo.username)):
        return JSONResponse(
            content={"message": "Please Enter Password and UserName"},
            status_code=400
        )
    
    if((not userInfo.authType) or (not userInfo.desigantion)):
        return JSONResponse(
            content={"message": "Please Enter Authtype and designation"},
            status_code=400
        )

    if(len(userInfo.mobileNumber)!=10 and len(userInfo.mobileNumber)!=0):
        return JSONResponse(
            content={"message": "Mobile Number should be 10 digits exactly!"},
            status_code=400
        )
    
    if not userInfo.fullName:
        return JSONResponse(
            content={"message": "Please Enter Full Name"},
            status_code=400
        )

    user=getUserByUserName(userInfo.username,db)

    if user is not None:
        return JSONResponse(
            content={"message": "User already exists"},
            status_code=400
        )
    
    newUser=createUser(userInfo,db)
    
    if not newUser:
        return JSONResponse(
            content={"message": "Error creating new User"},
            status_code=400
        )

    return JSONResponse(
        content={"message": "User created successfully"},
        status_code=201
    )

def deleteUserController(username:str,db:Session) -> JSONResponse:
    if not username:
        return JSONResponse(
            content={"message": "Please, Enter Username"},
            status_code=400
        )
    
    success=deleteUserByUsername(username,db)

    if success is None:
        return JSONResponse(
            content={"message": "User not found"},
            status_code=404
        )

    if(success):
        return JSONResponse(
            content={"message": "User deleted successfully"},
            status_code=200
        )
    
    return JSONResponse(
        content={"message": "Error deleting User"},
        status_code=400
    )