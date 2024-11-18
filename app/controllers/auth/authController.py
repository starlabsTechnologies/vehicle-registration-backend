from app.services.auth.authServices import getUserByUserName,logUserIn, createUser,deleteUserByUsername,authorizeUser,AuthResult
from app.models.userInfoBase import AuthorizeUser,UserInfoResponse,UserLogin,CreateUser,SuccessResponse,AuthResponse
# from app.schema.userInfo import UserInfo,AuthTypeEnum
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.utils.logger import logger

def authorizeUserController(userInfo:AuthorizeUser,db:Session) -> AuthResponse:
    try:
        user=authorizeUser(userInfo.username,userInfo.password,db)

        if user is AuthResult.USER_NOT_FOUND:
            logger.warning(f"User not found: {userInfo.username}")
            return JSONResponse(
                content={"message":"User Not Found","isAuthorized":False},
                status_code=404
            )
        
        if user is AuthResult.INCORRECT_PASSWORD:
            logger.warning("Incorrect Password")
            return JSONResponse(
                content={"message":"Incorrect Password","isAuthorized":False},
                status_code=401
            )
        
        if user is AuthResult.UNAUTHORIZED_ACCESS:
            logger.warning("Unauthorized Access")
            return JSONResponse(
                content={"message":"User is not authorized to change credentials.","isAuthorized":False},
                status_code=403
            )
        
        logger.info("User is Authorized")
        return AuthResponse(
            message="User is Authorized",
            isAuthorized=True
        )
    
    except Exception as error:
        logger.error(f"Error while authorizing user: {error}")
        return JSONResponse(
            content={"message": "Error while authorizing user"},
            status_code=500
        )

def logUserInController(userInfo:UserLogin,db:Session) -> UserInfoResponse:
    try:
        user=logUserIn(userInfo.username,userInfo.password,db)

        if user is None:
            logger.warning(f"User with username: {userInfo.username} not found")
            return JSONResponse(
                content={"message": "User Not Found"},
                status_code=404
            )
        
        if user is False:
            logger.warning("Incorrect password")
            return JSONResponse(
                content={"message": "Incorrect Password"},
                status_code=401
            )
        
        logger.info("User logged in")
        user.message = "User logged in"
        return user
    
    except Exception as error:
        logger.error(f"Error while logging user in: {error}")
        return JSONResponse(
            content={"message": "Error while logging user in"},
            status_code=500
        )

def createUserController(userInfo: CreateUser,db:Session) -> JSONResponse:
    try:
        if((not userInfo.password) or (not userInfo.username)):
            logger.warning("Please Enter Password and UserName")
            return JSONResponse(
                content={"message": "Please Enter Password and UserName"},
                status_code=400
            )
        
        if((not userInfo.authType) or (not userInfo.desigantion)):
            logger.warning("Please Enter Authtype and designation")
            return JSONResponse(
                content={"message": "Please Enter Authtype and designation"},
                status_code=400
            )

        if(len(userInfo.mobileNumber)!=10 and len(userInfo.mobileNumber)!=0):
            logger.warning("Mobile Number should be 10 digits exactly!")
            return JSONResponse(
                content={"message": "Mobile Number should be 10 digits exactly!"},
                status_code=400
            )
        
        if not userInfo.fullName:
            logger.warning("Please Enter Full Name")
            return JSONResponse(
                content={"message": "Please Enter Full Name"},
                status_code=400
            )

        user=getUserByUserName(userInfo.username,db)

        if user is not None:
            logger.warning(f"User with username {userInfo.username} already exists")
            return JSONResponse(
                content={"message": "User already exists"},
                status_code=400
            )
        
        newUser=createUser(userInfo,db)
        
        if not newUser:
            logger.warning("Error creating new User")
            return JSONResponse(
                content={"message": "Error creating new User"},
                status_code=400
            )

        logger.info(f"User created successfully: {userInfo.username}")
        return JSONResponse(
            content={"message": "User created successfully"},
            status_code=201
        )
    
    except Exception as error:
        logger.error(f"Error occurred while creating user: {error}")
        return JSONResponse(
            content={"message": "Error occurred while creating user"},
            status_code=500
        )

def deleteUserController(username:str,db:Session) -> JSONResponse:
    try:
        if not username:
            logger.warning("Please Enter Username")
            return JSONResponse(
                content={"message": "Please Enter Username"},
                status_code=400
            )
        
        success=deleteUserByUsername(username,db)

        if success is None:
            logger.warning(f"User {username} not found")
            return JSONResponse(
                content={"message": "User not found"},
                status_code=404
            )

        if(success):
            logger.info(f"User with username {username} deleted successfully")
            return JSONResponse(
                content={"message": "User deleted successfully"},
                status_code=200
            )
        
        logger.warning("Error deleting User")
        return JSONResponse(
            content={"message": "Error deleting User"},
            status_code=400
        )
    
    except Exception as error:
        logger.error(f"Error occurred while deleting user: {error}")
        return JSONResponse(
            content={"message": "Error deleting User"},
            status_code=500
        )