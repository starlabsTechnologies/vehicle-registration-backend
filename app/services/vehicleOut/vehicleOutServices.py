from sqlalchemy.orm import Session
from typing import Optional
from app.models.vehicleInOutBase import VehicleOutResponse
from app.schema.vehicleRegistration import VehicleRegistration
from app.schema.allotedTags import AllotedTags
from app.schema.vehicleInOut import VehicleInOut,BarrierStatusEnum
from datetime import datetime
from sqlalchemy import and_
from app.schema.vehicleInOutLogs import VehicleInOutLogs,ActionsTypeEnum

def getVehicleOut(rfidTag:str,db:Session) -> Optional[VehicleOutResponse]:
    tag=db.query(AllotedTags).filter_by(rfidTag=rfidTag).one_or_none()
    vehicle=db.query(VehicleRegistration).filter_by(rfidTag=rfidTag).one_or_none()

    if tag is None:
        return None
    
    if vehicle is None:
        return None
    
    if tag.blacklisted:
        message = "Vehicle Blocked"
    else:
        message = "Vehicle Allowed"

        validity_till_date = datetime.strptime(vehicle.validityTill, '%d/%m/%Y')

        if validity_till_date < datetime.now():
            message = "Vehicle's validity till expired"

        else:
            latest_record = (
                db.query(VehicleInOut)
                .filter(
                    and_(
                        VehicleInOut.rfidTag == rfidTag,
                        VehicleInOut.dateIn.isnot(None),
                        VehicleInOut.timeIn.isnot(None),
                        VehicleInOut.dateOut.is_(None),
                        VehicleInOut.timeOut.is_(None),
                    )
                )
                .order_by(VehicleInOut.dateIn.desc(), VehicleInOut.timeIn.desc())
                .first()
            )

            # print(latest_record)
            if not latest_record or latest_record.dateOut and latest_record.timeOut:
                message="Vehicle hasn't been In"

    return VehicleOutResponse(
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

def openBarrier(rfidTag:str,db:Session):
    latest_record = (
        db.query(VehicleInOut)
        .filter(
            and_(
                VehicleInOut.rfidTag == rfidTag,
                VehicleInOut.dateIn.isnot(None),
                VehicleInOut.timeIn.isnot(None),
                VehicleInOut.dateOut.is_(None),
                VehicleInOut.timeOut.is_(None),
            )
        )
        .order_by(VehicleInOut.dateIn.desc(), VehicleInOut.timeIn.desc())
        .first()
    )

    if latest_record is None:
        return None
    
    latest_record.dateOut = datetime.now().date(),
    latest_record.timeOut = datetime.now().time(),
    latest_record.barrierStatus = BarrierStatusEnum.OPEN

    db.commit()
    db.refresh(latest_record)

    return True

def updateVehicleInOutLogs(rfidTag:str,db:Session,actionByUsername:str) -> bool:
    vehicleInfo = db.query(VehicleRegistration).filter_by(rfidTag=rfidTag).one_or_none()

    if vehicleInfo is None:
        return None

    updateLogs = VehicleInOutLogs(
        rfidTag = vehicleInfo.rfidTag,
        vehicleNumber = vehicleInfo.vehicleNumber,
        typeOfVehicle = vehicleInfo.typeOfVehicle.name,
        action = ActionsTypeEnum.EDITED.value,
        actionBy = actionByUsername
    )

    db.add(updateLogs)
    db.commit()
    db.refresh(updateLogs)

    if(updateLogs):
        return True
    
    return False