from pydantic import BaseModel
from typing import Optional

class AuthorizeUser(BaseModel):
    username:str
    password:str

class BlockUser(BaseModel):
    rfidTag:str
    vehicleNo:str
    action:str

class SuccessResponse(BaseModel):
    message:str
    isAuthorized:Optional[bool]=False
    isBlocked:Optional[bool]=False