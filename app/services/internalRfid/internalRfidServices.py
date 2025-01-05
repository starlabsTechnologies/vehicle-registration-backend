from sqlalchemy.orm import Session
from app.schema.vehicleRegistration import VehicleRegistration
from app.schema.allotedTags import AllotedTags
from app.models.allotedTagsBase import CreateAllotedTag,ReceiptResponse
from app.models.vehicleRegistrationBase import CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,VehicleRegistrationResponse
from typing import Optional
from datetime import datetime
from app.schema.allotedTagsLogs import AllotedTagsLogs,ActionsTypeEnum
from app.schema.vehicleRegistrationLogs import VehicleRegistrationLogs
import random
import string
from enum import Enum

def generate_sales_order_no():
    date_part=datetime.now().strftime("%Y-%m-%d")
    random_number = ''.join(random.choices(string.digits, k=4))
    return f"STARLABS-{date_part}-PROJECT-{random_number}"

def generate_transaction_id(vehicle_no):
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{vehicle_no}{random_string}"

def getVehicleReg(rfidTag: str, db: Session) -> Optional[VehicleRegistrationResponse]:
    tag = db.query(AllotedTags).filter_by(rfidTag=rfidTag).one_or_none()
    vehicle = db.query(VehicleRegistration).filter_by(rfidTag=rfidTag).one_or_none()

    if vehicle is None:
        if tag is None:
            return VehicleRegistrationResponse(
                rfidTag=rfidTag,
                typeOfVehicle="TCT",  # Assuming VehicleTypeEnum has a None or default option
                vehicleNumber="",
                doNumber=None,
                transporter=None,
                driverOwner=None,
                weighbridgeNo=None,
                visitPurpose=None,
                placeToVisit=None,
                personToVisit=None,
                validityTill=None,
                section=None,
                registerDate="",
                registerTime="",
                message="Vehicle not alloted"
            )
        else:
            return None  # This case shouldn't happen if logic is consistent, but included for completeness
    
    message = "Not Allocated" if tag is None else "Allocated"

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
        registerTime=vehicle.registerTime,
        message=message
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

def createVehicleRegistrationLogs(vehicleInfo:CreateVehicleRegistration,db:Session,actionByUsername:str) -> bool:
    createVehicleRegLogs=VehicleRegistrationLogs(
        rfidTag = vehicleInfo.rfidTag,
        vehicleNumber = vehicleInfo.vehicleNumber,
        typeOfVehicle = vehicleInfo.typeOfVehicle,
        action = ActionsTypeEnum.CREATED.value,
        actionBy = actionByUsername
    )

    db.add(createVehicleRegLogs)
    db.commit()
    db.refresh(createVehicleRegLogs)

    if(createVehicleRegLogs):
        return True
    
    return False

def getAllotedTag(rfidTag:str,db:Session) -> Optional[ReceiptResponse]:
    tag=db.query(AllotedTags).filter_by(rfidTag=rfidTag).one_or_none()

    if tag is None:
        return None

    return ReceiptResponse(
        rfidTag=tag.rfidTag,
        typeOfVehicle=tag.typeOfVehicle,
        vehicleNumber=tag.vehicleNumber,
        salesOrder=tag.salesOrder,
        transationId=tag.transationId,
        userid=tag.userid,
        barrierGate=tag.barrierGate,
        salesType=tag.salesType,
        total=tag.total,
        due=tag.due,
        regDate=tag.regDate,
        regTime=tag.regTime
    )

def createAllotedTag(dataInfo:CreateAllotedTag,db:Session) -> Optional[ReceiptResponse]:
    newTag=AllotedTags(
        rfidTag=dataInfo.rfidTag,
        typeOfVehicle=dataInfo.typeOfVehicle,
        vehicleNumber = dataInfo.vehicleNumber,
        regDate = datetime.now().strftime("%d-%m-%Y"), 
        regTime = datetime.now().strftime("%H:%M:%S HRS"),
        salesOrder = generate_sales_order_no(),
        transationId = generate_transaction_id(dataInfo.vehicleNumber),
        userid = "VAIBHAV", 
        barrierGate = "NCL BINA PROJECT MAIN BARRIER",
        salesType = "RFID ALLOCATION",
        quantity = "1", 
        total = dataInfo.total,
        due = dataInfo.due
    )

    db.add(newTag)
    db.commit()
    db.refresh(newTag)

    if(newTag):
        return ReceiptResponse(
        rfidTag=newTag.rfidTag,
        typeOfVehicle=newTag.typeOfVehicle,
        vehicleNumber=newTag.vehicleNumber,
        salesOrder=newTag.salesOrder,
        transationId=newTag.transationId,
        userid=newTag.userid,
        barrierGate=newTag.barrierGate,
        salesType=newTag.salesType,
        total=newTag.total,
        due=dataInfo.due,
        regDate=newTag.regDate,
        regTime=newTag.regTime
    )
    
    return None

def createAllotedTagsLogs(dataInfo:CreateAllotedTag,db:Session,actionByUsername:str) -> bool:
    createLogs=AllotedTagsLogs(
        rfidTag = dataInfo.rfidTag,
        vehicleNumber = dataInfo.vehicleNumber,
        typeOfVehicle = dataInfo.typeOfVehicle,
        action = ActionsTypeEnum.CREATED.value,
        actionBy = actionByUsername
    )

    db.add(createLogs)
    db.commit()
    db.refresh(createLogs)

    if(createLogs):
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

def editVehicleRegLogs(vehicleInfo:EditVehicleRegistration,db:Session,actionByUsername:str) -> bool:
    editLogs=VehicleRegistrationLogs(
        rfidTag = vehicleInfo.rfidTag,
        vehicleNumber = vehicleInfo.vehicleNumber,
        typeOfVehicle = vehicleInfo.typeOfVehicle,
        action = ActionsTypeEnum.EDITED.value,
        actionBy = actionByUsername
    )

    db.add(editLogs)
    db.commit()
    db.refresh(editLogs)

    if(editLogs):
        return True
    
    return False

def deleteVehicleReg(vehicleInfo:DeleteVehicleRegistration,db:Session) -> bool:
    vehicleReg=db.query(VehicleRegistration).filter_by(rfidTag=vehicleInfo.rfidTag).one_or_none()

    if vehicleReg is None:
        return None
    
    db.delete(vehicleReg)
    db.commit()

    return True

def deleteVehicleRegLogs(vehicleInfo:DeleteVehicleRegistration,db:Session,actionByUsername:str) -> bool:
    delLogs=VehicleRegistrationLogs(
        rfidTag = vehicleInfo.rfidTag,
        vehicleNumber = vehicleInfo.vehicleNumber,
        action = ActionsTypeEnum.DELETED.value,
        actionBy = actionByUsername
    )

    db.add(delLogs)
    db.commit()
    db.refresh(delLogs)

    if(delLogs):
        return True
    
    return False