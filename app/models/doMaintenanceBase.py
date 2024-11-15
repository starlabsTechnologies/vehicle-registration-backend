from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateDONumber(BaseModel):
    doNumber:str
    weighbridgeNo:str
    transporter:str
    permissidoNameon:Optional[str]=None
    validThrough:Optional[str]=None
    validityTill:str
    allotedQty:float
    releasedQty:float
    doAddress:Optional[str]=None
    doRoute:Optional[str]=None
    salesOrder:Optional[str]=None
    customerId:Optional[str]=None
    mobileNumber:Optional[str]=None

class UpdateDONumber(BaseModel):
    doNumber:str
    weighbridgeNo:Optional[str]=None
    transporter:Optional[str]=None
    validityTill:Optional[str]=None
    allotedQty:Optional[float]=0.00
    releasedQty:Optional[float]=0.00
    doRoute:Optional[str]=None
    salesOrder:Optional[str]=None
    mobileNumber:Optional[str]=None

class DONumberResponse(BaseModel):
    id:str
    doNumber:str
    weighbridgeNo:str
    transporter:str
    permissidoNameon:Optional[str]=None
    validThrough:Optional[str]=None
    validityTill:str
    allotedQty:float
    releasedQty:float
    leftQty:float
    doAddress:Optional[str]=None
    doRoute:Optional[str]=None
    salesOrder:Optional[str]=None
    customerId:Optional[str]=None
    mobileNumber:Optional[str]=None

    class Config:
        orm_mode = True

class DeleteDONumber(BaseModel):
    doNumber:str

class SuccessResponse(BaseModel):
    message:str