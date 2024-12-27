from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.schema.vehicleInOut import VehicleInOut
from app.schema.vehicleRegistration import VehicleRegistration
from app.models.vehicleInOutBase import VehicleInOutResponse,SummaryFilter,WeighbridgeWiseFilter,ShiftWiseFilter,DoWiseFilter,VehicleTypeFilter,ValidityWiseFilter
from typing import List
from app.models.vehicleRegistrationBase import RegistrationDetailsResponse

def getSummary(filterInfo:SummaryFilter,db:Session) -> List[VehicleInOutResponse]:
    # filters = [
    #     VehicleInOut.dateIn>=filterInfo.dateIn,
    #     VehicleInOut.dateOut<=filterInfo.dateOut,
    #     VehicleInOut.timeIn>=filterInfo.timeIn,
    #     VehicleInOut.timeOut<=filterInfo.timeOut
    # ]

    filters = [
        condition
        for key, condition in {
            "dateIn": VehicleInOut.dateIn >= filterInfo.dateIn,
            "dateOut": VehicleInOut.dateOut <= filterInfo.dateOut,
            "timeIn": VehicleInOut.timeIn >= filterInfo.timeIn,
            "timeOut": VehicleInOut.timeOut <= filterInfo.timeOut,
        }.items()
        if getattr(filterInfo, key) != ''
    ]
    
    results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    return [
        VehicleInOutResponse(
            rfidTag=result.rfidTag,
            typeOfVehicle=result.typeOfVehicle,
            vehicleNumber=result.vehicleNumber,
            doNumber=result.doNumber,
            transporter=result.transporter,
            driverOwner=result.driverOwner,
            weighbridgeNo=result.weighbridgeNo,
            visitPurpose=result.visitPurpose,
            placeToVisit=result.placeToVisit,
            personToVisit=result.personToVisit,
            validityTill=result.validityTill,
            section=result.section,
            dateIn=result.dateIn, 
            timeIn=result.timeIn,
            user=result.user,
            shift=result.shift,
            dateOut=result.dateOut,
            timeOut=result.timeOut,
            gross=result.gross,
            tare=result.tare,
            net=result.net,
            barrierStatus=result.barrierStatus,
            challanNo=result.challanNo
        ) for result in results
    ]

def getWeighbridgeWise(filterInfo:WeighbridgeWiseFilter,db:Session) -> List[VehicleInOutResponse]:
    # filters = [
    #     VehicleInOut.dateIn>=filterInfo.dateIn,
    #     VehicleInOut.dateOut<=filterInfo.dateOut,
    #     VehicleInOut.timeIn>=filterInfo.timeIn,
    #     VehicleInOut.timeOut<=filterInfo.timeOut
    # ]

    filters = [
        condition
        for key, condition in {
            "dateIn": VehicleInOut.dateIn>=filterInfo.dateIn,
            "dateOut": VehicleInOut.dateOut<=filterInfo.dateOut,
            "timeIn": VehicleInOut.timeIn>=filterInfo.timeIn,
            "timeOut": VehicleInOut.timeOut<=filterInfo.timeOut,
        }.items()
        if getattr(filterInfo, key) != ''
    ]
    
    results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    return [
        VehicleInOutResponse(
            rfidTag=result.rfidTag,
            typeOfVehicle=result.typeOfVehicle,
            vehicleNumber=result.vehicleNumber,
            doNumber=result.doNumber,
            transporter=result.transporter,
            driverOwner=result.driverOwner,
            weighbridgeNo=result.weighbridgeNo,
            visitPurpose=result.visitPurpose,
            placeToVisit=result.placeToVisit,
            personToVisit=result.personToVisit,
            validityTill=result.validityTill,
            section=result.section,
            dateIn=result.dateIn, 
            timeIn=result.timeIn,
            user=result.user,
            shift=result.shift,
            dateOut=result.dateOut,
            timeOut=result.timeOut,
            gross=result.gross,
            tare=result.tare,
            net=result.net,
            barrierStatus=result.barrierStatus,
            challanNo=result.challanNo
        ) for result in results
    ]

def getShiftWise(filterInfo:ShiftWiseFilter,db:Session) -> List[VehicleInOutResponse]:
    # filters = [
    #     VehicleInOut.dateIn>=filterInfo.dateIn,
    #     VehicleInOut.dateOut<=filterInfo.dateOut
    # ]

    filters = [
        condition
        for key, condition in {
            "dateIn": VehicleInOut.dateIn>=filterInfo.dateIn,
            "dateOut": VehicleInOut.dateOut<=filterInfo.dateOut,
        }.items()
        if getattr(filterInfo, key) != ''
    ]
    
    results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    return [
        VehicleInOutResponse(
            rfidTag=result.rfidTag,
            typeOfVehicle=result.typeOfVehicle,
            vehicleNumber=result.vehicleNumber,
            doNumber=result.doNumber,
            transporter=result.transporter,
            driverOwner=result.driverOwner,
            weighbridgeNo=result.weighbridgeNo,
            visitPurpose=result.visitPurpose,
            placeToVisit=result.placeToVisit,
            personToVisit=result.personToVisit,
            validityTill=result.validityTill,
            section=result.section,
            dateIn=result.dateIn, 
            timeIn=result.timeIn,
            user=result.user,
            shift=result.shift,
            dateOut=result.dateOut,
            timeOut=result.timeOut,
            gross=result.gross,
            tare=result.tare,
            net=result.net,
            barrierStatus=result.barrierStatus,
            challanNo=result.challanNo
        ) for result in results
    ]

def getDoWise(filterInfo:DoWiseFilter,db:Session) -> List[VehicleInOutResponse]:
    # filters = [
    #     VehicleInOut.dateIn>=filterInfo.dateIn,
    #     VehicleInOut.dateOut<=filterInfo.dateOut,
    #     VehicleInOut.timeIn>=filterInfo.timeIn,
    #     VehicleInOut.timeOut<=filterInfo.timeOut
    # ]

    filters = [
        condition
        for key, condition in {
            "dateIn": VehicleInOut.dateIn>=filterInfo.dateIn,
            "dateOut": VehicleInOut.dateOut<=filterInfo.dateOut,
            "timeIn": VehicleInOut.timeIn>=filterInfo.timeIn,
            "timeOut": VehicleInOut.timeOut<=filterInfo.timeOut,
        }.items()
        if getattr(filterInfo, key) != ''
    ]
    
    results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    return [
        VehicleInOutResponse(
            rfidTag=result.rfidTag,
            typeOfVehicle=result.typeOfVehicle,
            vehicleNumber=result.vehicleNumber,
            doNumber=result.doNumber,
            transporter=result.transporter,
            driverOwner=result.driverOwner,
            weighbridgeNo=result.weighbridgeNo,
            visitPurpose=result.visitPurpose,
            placeToVisit=result.placeToVisit,
            personToVisit=result.personToVisit,
            validityTill=result.validityTill,
            section=result.section,
            dateIn=result.dateIn, 
            timeIn=result.timeIn,
            user=result.user,
            shift=result.shift,
            dateOut=result.dateOut,
            timeOut=result.timeOut,
            gross=result.gross,
            tare=result.tare,
            net=result.net,
            barrierStatus=result.barrierStatus,
            challanNo=result.challanNo
        ) for result in results
    ]

def getVehicleType(filterInfo:VehicleTypeFilter,db:Session) -> List[VehicleInOutResponse]:
    # filters = [
    #     VehicleInOut.dateIn>=filterInfo.dateIn,
    #     VehicleInOut.dateOut<=filterInfo.dateOut,
    #     VehicleInOut.timeIn>=filterInfo.timeIn,
    #     VehicleInOut.timeOut<=filterInfo.timeOut
    # ]

    filters = [
        condition
        for key, condition in {
            "dateIn": VehicleInOut.dateIn>=filterInfo.dateIn,
            "dateOut": VehicleInOut.dateOut<=filterInfo.dateOut,
            "timeIn": VehicleInOut.timeIn>=filterInfo.timeIn,
            "timeOut": VehicleInOut.timeOut<=filterInfo.timeOut,
        }.items()
        if getattr(filterInfo, key) != ''
    ]
    
    results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    return [
        VehicleInOutResponse(
            rfidTag=result.rfidTag,
            typeOfVehicle=result.typeOfVehicle,
            vehicleNumber=result.vehicleNumber,
            doNumber=result.doNumber,
            transporter=result.transporter,
            driverOwner=result.driverOwner,
            weighbridgeNo=result.weighbridgeNo,
            visitPurpose=result.visitPurpose,
            placeToVisit=result.placeToVisit,
            personToVisit=result.personToVisit,
            validityTill=result.validityTill,
            section=result.section,
            dateIn=result.dateIn, 
            timeIn=result.timeIn,
            user=result.user,
            shift=result.shift,
            dateOut=result.dateOut,
            timeOut=result.timeOut,
            gross=result.gross,
            tare=result.tare,
            net=result.net,
            barrierStatus=result.barrierStatus,
            challanNo=result.challanNo
        ) for result in results
    ]

def getValidityWise(filterInfo:ValidityWiseFilter,db:Session) -> List[VehicleInOutResponse]:
    # filters = [
    #     VehicleInOut.dateIn>=filterInfo.dateIn,
    #     VehicleInOut.dateOut<=filterInfo.dateOut,
    #     VehicleInOut.timeIn>=filterInfo.timeIn,
    #     VehicleInOut.timeOut<=filterInfo.timeOut
    # ]

    filters = [
        condition
        for key, condition in {
            "dateIn": VehicleInOut.dateIn>=filterInfo.dateIn,
            "dateOut": VehicleInOut.dateOut<=filterInfo.dateOut,
            "timeIn": VehicleInOut.timeIn>=filterInfo.timeIn,
            "timeOut": VehicleInOut.timeOut<=filterInfo.timeOut,
        }.items()
        if getattr(filterInfo, key) != ''
    ]
    
    results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    return [
        VehicleInOutResponse(
            rfidTag=result.rfidTag,
            typeOfVehicle=result.typeOfVehicle,
            vehicleNumber=result.vehicleNumber,
            doNumber=result.doNumber,
            transporter=result.transporter,
            driverOwner=result.driverOwner,
            weighbridgeNo=result.weighbridgeNo,
            visitPurpose=result.visitPurpose,
            placeToVisit=result.placeToVisit,
            personToVisit=result.personToVisit,
            validityTill=result.validityTill,
            section=result.section,
            dateIn=result.dateIn, 
            timeIn=result.timeIn,
            user=result.user,
            shift=result.shift,
            dateOut=result.dateOut,
            timeOut=result.timeOut,
            gross=result.gross,
            tare=result.tare,
            net=result.net,
            barrierStatus=result.barrierStatus,
            challanNo=result.challanNo
        ) for result in results
    ]

def getVehicleInOutData(db:Session) -> List[VehicleInOutResponse]:
    results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    return [
        VehicleInOutResponse(
            rfidTag=result.rfidTag,
            typeOfVehicle=result.typeOfVehicle,
            vehicleNumber=result.vehicleNumber,
            doNumber=result.doNumber,
            transporter=result.transporter,
            driverOwner=result.driverOwner,
            weighbridgeNo=result.weighbridgeNo,
            visitPurpose=result.visitPurpose,
            placeToVisit=result.placeToVisit,
            personToVisit=result.personToVisit,
            validityTill=result.validityTill,
            section=result.section,
            dateIn=result.dateIn, 
            timeIn=result.timeIn,
            user=result.user,
            shift=result.shift,
            dateOut=result.dateOut,
            timeOut=result.timeOut,
            gross=result.gross,
            tare=result.tare,
            net=result.net,
            barrierStatus=result.barrierStatus,
            challanNo=result.challanNo
        ) for result in results
    ]

def getRegistrationDetails(db:Session) -> List[RegistrationDetailsResponse]:
    results=db.query(VehicleRegistration).all()

    if len(results)==0:
        return []
    
    return [
        RegistrationDetailsResponse(
            rfidTag=result.rfidTag,
            typeOfVehicle=result.typeOfVehicle,
            vehicleNumber=result.vehicleNumber,
            doNumber=result.doNumber,
            transporter=result.transporter,
            driverOwner=result.driverOwner,
            weighbridgeNo=result.weighbridgeNo,
            visitPurpose=result.visitPurpose,
            placeToVisit=result.placeToVisit,
            personToVisit=result.personToVisit,
            validityTill=result.validityTill,
            section=result.section,
            registerDate=result.registerDate,
            registerTime=result.registerTime,
            user=result.user,
            shift=result.shift,
            loading=result.loading,
        ) for result in results
    ]