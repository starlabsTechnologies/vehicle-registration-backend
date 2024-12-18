from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from app.config.db_config import get_db
from app.models.allotedTagsBase import SuccessResponse, BlockUser
from app.controllers.blockUser.blockUserController import blockUserController

blockUser_router=APIRouter()

@blockUser_router.post('/block-user',response_model=SuccessResponse)
def blockUser(req:Request,userInfo:BlockUser,db:Session=Depends(get_db)):
    return blockUserController(req,userInfo,db)