from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class AuthTypeEnum(str,Enum):
    ADMIN = "Admin"
    USER = "User"
    MASTER = "Master"

class SuccessResponse(BaseModel):
    message:str

class UserLogin(BaseModel):
    username:str
    password:str

class CreateUser(BaseModel):
    username:str
    password:str
    authType:AuthTypeEnum
    empId:Optional[str]=None
    fullName:Optional[str]=None
    email:Optional[str]=None
    desigantion:Optional[str]=None
    Address:Optional[str]=None
    mobileNumber:Optional[str]=None
    organisation:Optional[str]=None

class UserInfoResponse(BaseModel):
    id:str
    username:str
    password:str
    authType:AuthTypeEnum
    empId:Optional[str]=None
    fullName:Optional[str]=None
    email:Optional[str]=None
    desigantion:Optional[str]=None
    Address:Optional[str]=None
    mobileNumber:Optional[str]=None
    organisation:Optional[str]=None
    createdAt:datetime
    updatedAt:datetime

    class Config:
        orm_mode = True

class DeleteUser(BaseModel):
    username:str