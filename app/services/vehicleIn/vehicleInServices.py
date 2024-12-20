from sqlalchemy.orm import Session
from typing import Optional
from app.models.vehicleInOutBase import VehicleInResponse
from app.schema.allotedTags import AllotedTags
from app.schema.vehicleInOut import VehicleInOut
from app.models.vehicleInOutBase import VehicleInOutResponse

def getVehicleIn(rfidTag:str,db:Session) -> Optional[VehicleInResponse]:
    tag=db.query(AllotedTags).filter_by(rfidTag=rfidTag).one_or_none()
    vehicle=db.query(VehicleInOut).filter_by(rfidTag=rfidTag).one_or_none()

    if vehicle is None:
        return None
    
    if tag is None:
        return None
    
    if tag.blacklisted:
        message = "Vehicle Blocked"
    else:
        message = "Vehicle Allowed"

    return VehicleInResponse(
        rfidTag=vehicle.rfidTag,
        typeOfVehicle=vehicle.typeOfVehicle,
        vehicleNumber=vehicle.vehicleNumber,
        validityTill=vehicle.validityTill,
        doNumber=vehicle.doNumber,
        transporter=vehicle.transporter,
        driverOwner=vehicle.driverOwner,
        weighbridgeNo=vehicle.weighbridgeNo,
        visitPurpose=vehicle.visitPurpose,
        placeToVisit=vehicle.placeToVisit,
        personToVisit=vehicle.personToVisit,
        shift=vehicle.shift,
        section=vehicle.section,
        status=message
    )
    