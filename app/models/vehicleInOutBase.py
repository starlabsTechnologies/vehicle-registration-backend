from pydantic import BaseModel
from enum import Enum
from typing import Optional

class VehicleTypeEnum(str,Enum):  # Using Python's Enum class
    TCT = "TCT"
    PDV = "PDV"
    TVV = "TVV"
    TOV = "TOV"
    PCT = "PCT"
    TDBEV = "TDBEV"
    SCRAPE = "SCRAPE"

class BarrierStatusEnum(str,Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

class OptionsEnum(str,Enum):
    Summary = "Summary"
    WeighbridgeWise = "Weighbridge Wise"
    ShiftWise = "Shift Wise"
    DoWise = "Do Wise"
    VehicleType = "Vehicle Type"
    ValidityWise = "Validity Wise"
    RegistrationDetails = "Registration Details"

class DataFilter(BaseModel):
    option:OptionsEnum
    dateIn:Optional[str]=None
    dateOut:Optional[str]=None
    timeIn:Optional[str]=None
    timeOut:Optional[str]=None
    typeOfVehicle:Optional[VehicleTypeEnum]

class SummaryFilter(BaseModel):
    dateIn:str
    dateOut:str
    timeIn:str
    timeOut:str

class WeighbridgeWiseFilter(BaseModel):
    dateIn:str
    dateOut:str
    timeIn:str
    timeOut:str
    typeOfVehicle:VehicleTypeEnum

class ShiftWiseFilter(BaseModel):
    dateIn:str
    dateOut:str
    typeOfVehicle:VehicleTypeEnum

class DoWiseFilter(BaseModel):
    dateIn:str
    dateOut:str
    timeIn:str
    timeOut:str
    typeOfVehicle:VehicleTypeEnum

class VehicleTypeFilter(BaseModel):
    dateIn:str
    dateOut:str
    timeIn:str
    timeOut:str
    typeOfVehicle:VehicleTypeEnum

class ValidityWiseFilter(BaseModel):
    dateIn:str
    dateOut:str
    timeIn:str
    timeOut:str
    typeOfVehicle:VehicleTypeEnum

class VehicleInOutResponse(BaseModel):
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
    dateIn:str  
    timeIn:str
    user:Optional[str]=None
    shift:Optional[str]=None
    dateOut:Optional[str]=None
    timeOut:Optional[str]=None
    gross:Optional[float]=0.00
    tare:Optional[float]=0.00
    net:Optional[float]=0.00
    barrierStatus:Optional[BarrierStatusEnum] = BarrierStatusEnum.CLOSED
    challanNo:Optional[str]=None

    class Config:
        orm_mode = True