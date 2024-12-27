from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.schema.vehicleInOut import VehicleInOut
from app.schema.vehicleRegistration import VehicleRegistration
from app.models.vehicleInOutBase import VehicleInOutResponse,SummaryFilter,WeighbridgeWiseFilter,ShiftWiseFilter,DoWiseFilter,VehicleTypeFilter,ValidityWiseFilter,PaginatedVehicleInOutResponse
from typing import List
from app.models.vehicleRegistrationBase import RegistrationDetailsResponse,PaginatedRegResponse
import math

def getSummary(filterInfo:SummaryFilter,db:Session,page: int = 1,pageSize: int =1) -> PaginatedVehicleInOutResponse:
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

    offset = (page - 1) * pageSize
    limit = pageSize
    
    total_records = db.query(VehicleInOut).filter(and_(*filters)).count()

    results = (db.query(VehicleInOut).filter(and_(*filters)).offset(offset).limit(limit).all())

    total_pages = math.ceil(total_records / pageSize)

    # results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    data = [
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

    return PaginatedVehicleInOutResponse(
        totalPages=total_pages,
        data=data,
    )

def getWeighbridgeWise(filterInfo:WeighbridgeWiseFilter,db:Session,page: int = 1,pageSize: int =1) -> PaginatedVehicleInOutResponse:
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

    offset = (page - 1) * pageSize
    limit = pageSize
    
    total_records = db.query(VehicleInOut).filter(and_(*filters)).count()

    results = (db.query(VehicleInOut).filter(and_(*filters)).offset(offset).limit(limit).all())

    total_pages = math.ceil(total_records / pageSize)
    
    # results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    data = [
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

    return PaginatedVehicleInOutResponse(
        totalPages=total_pages,
        data=data,
    )

def getShiftWise(filterInfo:ShiftWiseFilter,db:Session,page: int = 1,pageSize: int =1) -> PaginatedVehicleInOutResponse:
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

    offset = (page - 1) * pageSize
    limit = pageSize
    
    total_records = db.query(VehicleInOut).filter(and_(*filters)).count()

    results = (db.query(VehicleInOut).filter(and_(*filters)).offset(offset).limit(limit).all())

    total_pages = math.ceil(total_records / pageSize)
    
    # results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    data = [
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

    return PaginatedVehicleInOutResponse(
        totalPages=total_pages,
        data=data,
    )

def getDoWise(filterInfo:DoWiseFilter,db:Session,page: int = 1,pageSize: int =1) -> PaginatedVehicleInOutResponse:
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

    offset = (page - 1) * pageSize
    limit = pageSize
    
    total_records = db.query(VehicleInOut).filter(and_(*filters)).count()

    results = (db.query(VehicleInOut).filter(and_(*filters)).offset(offset).limit(limit).all())

    total_pages = math.ceil(total_records / pageSize)
    
    # results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    data = [
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

    return PaginatedVehicleInOutResponse(
        totalPages=total_pages,
        data=data,
    )

def getVehicleType(filterInfo:VehicleTypeFilter,db:Session,page: int = 1,pageSize: int =1) -> PaginatedVehicleInOutResponse:
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

    offset = (page - 1) * pageSize
    limit = pageSize
    
    total_records = db.query(VehicleInOut).filter(and_(*filters)).count()

    results = (db.query(VehicleInOut).filter(and_(*filters)).offset(offset).limit(limit).all())

    total_pages = math.ceil(total_records / pageSize)
    
    # results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    data = [
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

    return PaginatedVehicleInOutResponse(
        totalPages=total_pages,
        data=data,
    )

def getValidityWise(filterInfo:ValidityWiseFilter,db:Session,page: int = 1,pageSize: int =1) -> PaginatedVehicleInOutResponse:
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

    offset = (page - 1) * pageSize
    limit = pageSize
    
    total_records = db.query(VehicleInOut).filter(and_(*filters)).count()

    results = (db.query(VehicleInOut).filter(and_(*filters)).offset(offset).limit(limit).all())

    total_pages = math.ceil(total_records / pageSize)
    
    # results=db.query(VehicleInOut).filter(and_(*filters)).all()
    # results=db.query(VehicleInOut).all()

    if len(results)==0:
        return []
    
    data = [
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

    return PaginatedVehicleInOutResponse(
        totalPages=total_pages,
        data=data,
    )

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

def getRegistrationDetails(db:Session,page: int = 1,pageSize: int =1) -> PaginatedRegResponse:
    # results=db.query(VehicleRegistration).all()

    offset = (page - 1) * pageSize
    limit = pageSize
    
    total_records = db.query(VehicleRegistration).count()

    results = (db.query(VehicleRegistration)).offset(offset).limit(limit).all()

    total_pages = math.ceil(total_records / pageSize)

    if len(results)==0:
        return []
    
    data = [
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

    return PaginatedRegResponse(
        totalPages=total_pages,
        data=data,
    )