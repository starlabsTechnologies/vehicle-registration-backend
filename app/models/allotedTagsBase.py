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

class DueAmount(BaseModel):
    due:str

class BlockUser(BaseModel):
    rfidTag:str
    vehicleNo:str
    action:str

class SuccessResponse(BaseModel):
    message:str
    isBlocked:Optional[bool]=False

class NewAllotedReceiptResponse(BaseModel):
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
    due:bool
    message:Optional[str]=None

class ReceiptResponse(BaseModel):
    rfidTag:str
    typeOfVehicle:VehicleTypeEnum
    vehicleNumber:str
    salesOrder: str  # Add this field
    transationId: str  # Add this field if it's not already there
    total:str
    regDate:str
    regTime:str  
    userid:str
    barrierGate:str
    salesType:str
    due:bool
    message:Optional[str]=None

class CreateAllotedTag(BaseModel):
    rfidTag:str
    typeOfVehicle:VehicleTypeEnum
    vehicleNumber:str
    total:str
    due:bool