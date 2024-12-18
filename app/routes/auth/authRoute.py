from fastapi import APIRouter, Depends,Request
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.userInfoBase import UserInfoResponse,UserLogin,CreateUser,SuccessResponse,AuthorizeUser,AuthResponse
from app.controllers.auth.authController import logUserInController,createUserController,deleteUserController,authorizeUserController

auth_router=APIRouter()

@auth_router.post('/login',response_model=UserInfoResponse)
def login(userInfo:UserLogin,db:Session=Depends(get_db)):
    return logUserInController(userInfo,db)

@auth_router.post('/auth-user',response_model=AuthResponse)
def authUser(userInfo:AuthorizeUser,db:Session=Depends(get_db)):
    return authorizeUserController(userInfo,db)

@auth_router.post('/user',response_model=SuccessResponse)
def createuser(req:Request,userInfo:CreateUser,db:Session=Depends(get_db)):
    return createUserController(req,userInfo,db)

@auth_router.delete('/user/{username}',response_model=SuccessResponse)
def deleteuser(req:Request,username:str,db:Session=Depends(get_db)):
    return deleteUserController(req,username,db)

# {         
# "username": "rashmi",         
# "password": "123",        
# "authType": "Master",         
# "empId": "1234574257",         
# "fullName": "VAIBHAV",         
# "email": "email@email.com",         
# "desigantion": "Something",         
# "Address": "My address",         
# "mobileNumber": "1234567890",         
# "organisation": "This organiztion"       
# }