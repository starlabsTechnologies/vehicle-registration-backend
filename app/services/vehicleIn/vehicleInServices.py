from sqlalchemy.orm import Session
from typing import Optional
from app.models.vehicleInOutBase import VehicleInResponse
from app.schema.vehicleRegistration import VehicleRegistration,VehicleTypeEnum
from app.schema.allotedTags import AllotedTags
from app.schema.vehicleInOut import VehicleInOut
from datetime import datetime
from sqlalchemy import and_
from app.schema.vehicleInOutLogs import VehicleInOutLogs,ActionsTypeEnum

def getVehicleIn(rfidTag:str,db:Session) -> Optional[VehicleInResponse]:
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

        if message != "Vehicle's validity till expired":
            latest_in_record = (
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
            # latest_in_record = db.query(VehicleInOut).filter_by(rfidTag=rfidTag).order_by(VehicleInOut.dateIn.desc(), VehicleInOut.timeIn.desc()).first()

            print(latest_in_record)
            if latest_in_record and not latest_in_record.timeOut and not latest_in_record.dateOut:
                message="Vehicle is already In"

            # if latest_in_record.dateOut and latest_out_record.timeOut:
            #     if latest_in_record.dateIn > latest_out_record.dateOut and latest_in_record.timeIn > latest_in_record.timeOut:
            #         message="Vehicle is already In"

            else:
                newVehicleIn=VehicleInOut(
                    rfidTag=vehicle.rfidTag,
                    typeOfVehicle=vehicle.typeOfVehicle.name,
                    vehicleNumber=vehicle.vehicleNumber,
                    doNumber=vehicle.doNumber,
                    transporter=vehicle.transporter,
                    driverOwner=vehicle.driverOwner,
                    weighbridgeNo=vehicle.weighbridgeNo,
                    visitPurpose=vehicle.visitPurpose,
                    placeToVisit=vehicle.placeToVisit,
                    personToVisit=vehicle.personToVisit,
                    validityTill=vehicle.validityTill,
                    section=vehicle.section,
                    dateIn = datetime.now().date(),
                    timeIn = datetime.now().time()
                )

                db.add(newVehicleIn)
                db.commit()
                db.refresh(newVehicleIn)

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
    
def updateVehicleInOutLogs(rfidTag:str,db:Session,actionByUsername:str) -> bool:
    vehicleInfo = db.query(VehicleRegistration).filter_by(rfidTag=rfidTag).one_or_none()

    if vehicleInfo is None:
        return None

    updateLogs = VehicleInOutLogs(
        rfidTag = vehicleInfo.rfidTag,
        vehicleNumber = vehicleInfo.vehicleNumber,
        typeOfVehicle = vehicleInfo.typeOfVehicle.name,
        action = ActionsTypeEnum.CREATED.value,
        actionBy = actionByUsername
    )

    db.add(updateLogs)
    db.commit()
    db.refresh(updateLogs)

    if(updateLogs):
        return True
    
    return False