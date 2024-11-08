from pydantic import BaseModel
from datetime import time, datetime

class ShiftTimingUpdate(BaseModel):
    shift_name:str
    from_time:time
    to_time:time

class ShiftTimingResponse(BaseModel):
    id:str
    shift_name:str
    from_time:time
    to_time:time
    createdAt:datetime
    updatedAt:datetime

    class Config:
        orm_mode = True