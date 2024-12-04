from pydantic import BaseModel, Field,root_validator
from enum import Enum
from typing import Optional
from datetime import datetime

class VehicleTypeEnum(str,Enum):  # Using Python's Enum class
    TCT = "TCT"
    PDV = "PDV"
    TVV = "TVV"
    TOV = "TOV"
    PCT = "PCT"
    TDBEV = "TDBEV"
    SCRAPE = "SCRAPE"

class RegistrationDetailsResponse(BaseModel):
    rfidTag:str
    typeOfVehicle:VehicleTypeEnum
    vehicleNumber:str
    doNumber:Optional[str]=None
    transporter:Optional[str]=None
    driverOwner:Optional[str]=None
    weighbridgeNo:Optional[str]=None
    visitPurpose:Optional[str]=None
    placeToVisit:Optional[str]=None
    personToVisit:Optional[str]=None
    validityTill:Optional[str]=None
    section:Optional[str]=None
    registerDate:str
    registerTime:str
    user:Optional[str]=None
    shift:Optional[str]=None
    loading:Optional[str]=None

class SuccessResponse(BaseModel):
    message:str

class CreateVehicleRegistration(BaseModel):
    rfidTag:str
    typeOfVehicle:VehicleTypeEnum
    vehicleNumber:str
    doNumber:Optional[str]=None
    transporter:Optional[str]=None
    driverOwner:Optional[str]=None
    weighbridgeNo:Optional[str]=None
    visitPurpose:Optional[str]=None
    placeToVisit:Optional[str]=None
    personToVisit:Optional[str]=None
    validityTill:str
    total:str
    section:Optional[str]=None
    registerDate: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    registerTime: str = Field(default_factory=lambda: datetime.now().strftime('%H:%M:%S'))

    @root_validator(pre=True)
    def enforce_current_datetime(cls, values):
        values['registerDate'] = datetime.now().strftime('%Y-%m-%d')
        values['registerTime'] = datetime.now().strftime('%H:%M:%S')
        return values

class EditVehicleRegistration(BaseModel):
    rfidTag:str
    typeOfVehicle:VehicleTypeEnum
    vehicleNumber:Optional[str]=None
    doNumber:Optional[str]=None
    transporter:Optional[str]=None
    driverOwner:Optional[str]=None
    weighbridgeNo:Optional[str]=None
    visitPurpose:Optional[str]=None
    placeToVisit:Optional[str]=None
    personToVisit:Optional[str]=None
    validityTill:Optional[str]=None
    section:Optional[str]=None

class DeleteVehicleRegistration(BaseModel):
    rfidTag:str
    vehicleNumber:Optional[str]=None

class VehicleRegistrationResponse(BaseModel):
    rfidTag:str
    typeOfVehicle:VehicleTypeEnum
    vehicleNumber:str
    doNumber:Optional[str]=None
    transporter:Optional[str]=None
    driverOwner:Optional[str]=None
    weighbridgeNo:Optional[str]=None
    visitPurpose:Optional[str]=None
    placeToVisit:Optional[str]=None
    personToVisit:Optional[str]=None
    validityTill:Optional[str]=None
    section:Optional[str]=None
    registerDate:str
    registerTime:str
    
    # New Fields
    # registerDate:Optional[str]=None  
    # registerTime:Optional[str]=None
    # user:Optional[str]=None
    # shift:Optional[str]=None
    # loading:Optional[str]=None

    class Config:
        orm_mode = True