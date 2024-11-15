from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.config.db_config import get_db
from app.controllers.changePass.changePassController import getUserController,editUserController
from app.models.userInfoBase import EditUser,SuccessResponse,UserInfoResponse

changePass_router=APIRouter()

#Use blockUser_router('/auth-user)

@changePass_router.get('/change-pass/{username}',response_model=UserInfoResponse)
def getUser(username:str,db:Session=Depends(get_db)):
    return getUserController(username,db)

@changePass_router.put('/change-pass',response_model=SuccessResponse)
def editUser(userInfo:EditUser,db:Session=Depends(get_db)):
    return editUserController(userInfo,db)


# {
#   "username": "dfd",
#   "password": "fdfd",
#   "fullName": "string",
#   "email": "fd",
#   "Address": "dfdd",
#   "mobileNumber": "9876543211"
# }