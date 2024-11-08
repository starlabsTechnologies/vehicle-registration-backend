from fastapi import APIRouter, Depends
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.userInfoBase import UserInfoResponse,UserLogin,CreateUser,SuccessResponse
from app.controllers.auth.authController import logUserInController,createUserController,deleteUserController

auth_router=APIRouter()

@auth_router.post('/login',response_model=UserInfoResponse)
def login(userInfo:UserLogin,db:Session=Depends(get_db)):
    return logUserInController(userInfo,db)

@auth_router.post('/user',response_model=SuccessResponse)
def createuser(userInfo:CreateUser,db:Session=Depends(get_db)):
    return createUserController(userInfo,db)

@auth_router.delete('/user/{username}',response_model=SuccessResponse)
def deleteuser(username:str,db:Session=Depends(get_db)):
    return deleteUserController(username,db)

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