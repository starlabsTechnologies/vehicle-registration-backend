from pydantic import BaseModel
from typing import Optional
from enum import Enum

class VehicleTypeEnum(str,Enum):  # Using Python's Enum class
    TCT = "TCT"
    PDV = "PDV"
    TVV = "TVV"
    TOV = "TOV"
    PCT = "PCT"
    TDBEV = "TDBEV"
    SCRAPE = "SCRAPE"

class BlockUser(BaseModel):
    rfidTag:str
    vehicleNo:str
    action:str

class ServiceResponse(BaseModel):
    success:Optional[bool]=False
    rfid:Optional[str]=None

class SuccessResponse(BaseModel):
    message:str
    isBlocked:Optional[bool]=False

class ReceiptResponse(BaseModel):
    rfidTag:str
    typeOfVehicle:VehicleTypeEnum
    vehicleNumber:str
    regDate:str
    regTime:str
    salesOrder:str 
    transationId:str  
    userid:str
    barrierGate:str
    salesType:str
    total:str
    message:Optional[str]=None

class CreateAllotedTag(BaseModel):
    rfidTag:str
    typeOfVehicle:VehicleTypeEnum
    vehicleNumber:str
    total:str