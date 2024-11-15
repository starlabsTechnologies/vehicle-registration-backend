from sqlalchemy.orm import Session
from app.schema.vehicleRegistration import VehicleRegistration
from app.models.vehicleRegistrationBase import CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,VehicleRegistrationResponse
from typing import Optional

def getVehicleReg(rfidTag:str,db:Session) -> Optional[VehicleRegistrationResponse]:
    vehicle=db.query(VehicleRegistration).filter_by(rfidTag=rfidTag).one_or_none()

    if vehicle is None:
        return None

    return VehicleRegistrationResponse(
        rfidTag=vehicle.rfidTag,
        typeOfVehicle=vehicle.typeOfVehicle,
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
        registerDate=vehicle.registerDate,
        registerTime=vehicle.registerTime
    )

def createVehicleReg(vehicleInfo:CreateVehicleRegistration,db:Session) -> bool:
    newReg=VehicleRegistration(
        rfidTag=vehicleInfo.rfidTag,
        typeOfVehicle=vehicleInfo.typeOfVehicle,
        vehicleNumber=vehicleInfo.vehicleNumber,
        doNumber=vehicleInfo.doNumber,
        transporter=vehicleInfo.transporter,
        driverOwner=vehicleInfo.driverOwner,
        weighbridgeNo=vehicleInfo.weighbridgeNo,
        visitPurpose=vehicleInfo.visitPurpose,
        placeToVisit=vehicleInfo.placeToVisit,
        personToVisit=vehicleInfo.personToVisit,
        validityTill=vehicleInfo.validityTill,
        section=vehicleInfo.section,
        registerDate=vehicleInfo.registerDate,
        registerTime=vehicleInfo.registerTime
    )

    db.add(newReg)
    db.commit()
    db.refresh(newReg)

    if(newReg):
        return True
    
    return False

def editVehicleReg(vehicleInfo:EditVehicleRegistration,db:Session) -> bool:
    vehicleReg=db.query(VehicleRegistration).filter_by(rfidTag=vehicleInfo.rfidTag).one_or_none()

    if vehicleReg is None:
        return None
    
    vehicleReg.vehicleNumber=vehicleInfo.vehicleNumber,
    vehicleReg.doNumber=vehicleInfo.doNumber,
    vehicleReg.transporter=vehicleInfo.transporter,
    vehicleReg.driverOwner=vehicleInfo.driverOwner,
    vehicleReg.weighbridgeNo=vehicleInfo.weighbridgeNo,
    vehicleReg.visitPurpose=vehicleInfo.visitPurpose,
    vehicleReg.placeToVisit=vehicleInfo.placeToVisit,
    vehicleReg.personToVisit=vehicleInfo.personToVisit,
    vehicleReg.validityTill=vehicleInfo.validityTill,
    vehicleReg.section=vehicleInfo.section

    db.commit()
    db.refresh(vehicleReg)

    return True

def deleteVehicleReg(vehicleInfo:DeleteVehicleRegistration,db:Session) -> bool:
    vehicleReg=db.query(VehicleRegistration).filter_by(rfidTag=vehicleInfo.rfidTag).one_or_none()

    if vehicleReg is None:
        return None
    
    db.delete(vehicleReg)
    db.commit()

    return True