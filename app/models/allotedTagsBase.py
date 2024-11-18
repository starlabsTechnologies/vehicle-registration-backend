from pydantic import BaseModel
from typing import Optional

class BlockUser(BaseModel):
    rfidTag:str
    vehicleNo:str
    action:str

class SuccessResponse(BaseModel):
    message:str
    isBlocked:Optional[bool]=False