from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.config.db_config import get_db
from app.models.allotedTagsBase import SuccessResponse, AuthorizeUser, BlockUser
from app.controllers.blockUser.blockUserController import authorizeUserController,blockUserController

blockUser_router=APIRouter()

@blockUser_router.post('/auth-user',response_model=SuccessResponse)
def authUser(userInfo:AuthorizeUser,db:Session=Depends(get_db)):
    return authorizeUserController(userInfo,db)

@blockUser_router.post('/block-user',response_model=SuccessResponse)
def blockUser(userInfo:BlockUser,db:Session=Depends(get_db)):
    return blockUserController(userInfo,db)


# {
#   "rfidTag": "1",
#   "vehicleNo": "1",
#   "action": "Blacklist"
# }