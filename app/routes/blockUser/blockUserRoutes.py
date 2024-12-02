from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.config.db_config import get_db
from app.models.allotedTagsBase import SuccessResponse, BlockUser, ServiceResponse
from app.controllers.blockUser.blockUserController import blockUserController,getRfidFromServiceController

blockUser_router=APIRouter()

@blockUser_router.post('/block-user',response_model=SuccessResponse)
def blockUser(userInfo:BlockUser,db:Session=Depends(get_db)):
    return blockUserController(userInfo,db)

@blockUser_router.get('/rfid-connect',response_model=ServiceResponse)
async def fetchRfidTag():
    return await getRfidFromServiceController()

# {
#   "rfidTag": "1",
#   "vehicleNo": "1",
#   "action": "Blacklist"
# }