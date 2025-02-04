from pydantic import BaseModel
from typing import Optional
from enum import Enum

class AuthTypeEnum(str,Enum):
    ADMIN = "Admin"
    USER = "User"
    MASTER = "Master"

class ActiveStatusTypeEnum(str,Enum):
    ACTIVE = "active"
    LOGOUT = "logout"
    DELETED = "deleted"
    DEACTIVATED = "deactivated"

class AuthorizeUser(BaseModel):
    username:str
    password:str

class SuccessResponse(BaseModel):
    message:str

class AuthResponse(BaseModel):
    message:str
    isAuthorized:Optional[bool]=False

class UserLogout(BaseModel):
    username:str

class CreateUser(BaseModel):
    username:str
    password:str
    authType:AuthTypeEnum
    empId:Optional[str]=None
    fullName:str
    email:Optional[str]=None
    desigantion:str
    Address:Optional[str]=None
    mobileNumber:Optional[str]=None
    organisation:Optional[str]=None

class EditUser(BaseModel):
    username:str
    password:str
    fullName:str
    email:str
    Address:str
    mobileNumber:str

class UserInfoResponse(BaseModel):
    id:str
    username:str
    authType:AuthTypeEnum
    empId:Optional[str]=None
    fullName:Optional[str]=None
    email:Optional[str]=None
    desigantion:Optional[str]=None
    Address:Optional[str]=None
    mobileNumber:Optional[str]=None
    organisation:Optional[str]=None
    message:Optional[str]=None

    class Config:
        orm_mode = True

class DeleteUser(BaseModel):
    username:str