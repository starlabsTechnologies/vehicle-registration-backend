from sqlalchemy.orm import Session
from app.schema.doMaintenance import DoData
from app.models.doMaintenanceBase import CreateDONumber,DONumberResponse, UpdateDONumber
from app.schema.do_logs import DoLog
from enum import Enum

class ActionsTypeEnum(Enum):  # Using Python's Enum class
    DELETED = "DELETED"
    CREATED = "CREATED"
    EDITED = "EDITED"

def getDoDataByDoNumber(doNumber:str,db:Session) -> DONumberResponse:
    doData=db.query(DoData).filter_by(doNumber=doNumber).one_or_none()

    if doData is None:
        return None
    
    return DONumberResponse(
        id=str(doData.id),
        doNumber=doData.doNumber,
        weighbridgeNo=doData.weighbridgeNo,
        transporter=doData.transporter,
        permissidoNameon=doData.permissidoNameon,
        validThrough=doData.validThrough,
        validityTill=doData.validityTill,
        allotedQty=doData.allotedQty,
        releasedQty=doData.releasedQty,
        leftQty=doData.leftQty,
        doAddress=doData.doAddress,
        doRoute=doData.doRoute,
        salesOrder=doData.salesOrder,
        customerId=doData.customerId,
        mobileNumber=doData.mobileNumber,
        createdAt=doData.createdAt,
        updatedAt=doData.updatedAt
    )

def createDONumber(doInfo:CreateDONumber,db:Session) -> bool:   
    newDoData=DoData(
        doNumber=doInfo.doNumber,
        weighbridgeNo=doInfo.weighbridgeNo,
        transporter=doInfo.transporter,
        permissidoNameon=doInfo.permissidoNameon,
        validThrough=doInfo.validThrough,
        validityTill=doInfo.validityTill,
        allotedQty=doInfo.allotedQty,
        releasedQty=doInfo.releasedQty,
        leftQty=doInfo.allotedQty-doInfo.releasedQty,
        doAddress=doInfo.doAddress,
        doRoute=doInfo.doRoute,
        salesOrder=doInfo.salesOrder,
        customerId=doInfo.customerId,
        mobileNumber=doInfo.mobileNumber
    )

    db.add(newDoData)
    db.commit()
    db.refresh(newDoData)

    if(newDoData):
        return True
    
    return False

def createDONumberLogs(doInfo:CreateDONumber,db:Session,actionByUsername:str) -> bool:
    createDONumberLog = DoLog(
        doNumber=doInfo.doNumber,
        weighbridgeNo=doInfo.weighbridgeNo,
        transporter=doInfo.transporter,
        action=ActionsTypeEnum.CREATED.value,
        actionBy=actionByUsername,
    )

    db.add(createDONumberLog)
    db.commit()
    db.refresh(createDONumberLog)

    if(createDONumberLog):
        return True
    
    return False

def updateDONumber(doInfo:UpdateDONumber,db:Session) -> bool:
    doData=db.query(DoData).filter_by(doNumber=doInfo.doNumber).one_or_none()

    if doData is None:
        return False
    
    doData.weighbridgeNo=doInfo.weighbridgeNo
    doData.transporter=doInfo.transporter
    doData.validityTill=doInfo.validityTill
    doData.allotedQty=doInfo.allotedQty
    doData.releasedQty=doInfo.releasedQty
    doData.doRoute=doInfo.doRoute
    doData.salesOrder=doInfo.salesOrder
    doData.mobileNumber=doInfo.mobileNumber

    db.commit()
    return True

def updateDONumberLogs(doInfo:CreateDONumber,db:Session,actionByUsername:str) -> bool:
    updateDONumberLog= DoLog(
        doNumber=doInfo.doNumber,
        weighbridgeNo=doInfo.weighbridgeNo,
        transporter=doInfo.transporter,
        action=ActionsTypeEnum.EDITED.value,
        actionBy=actionByUsername,
    )

    db.add(updateDONumberLog)
    db.commit()
    db.refresh(updateDONumberLog)

    if(updateDONumberLog):
        return True
    
    return False

def deleteDONumber(doNumber:str,db:Session) -> bool:
    doData=db.query(DoData).filter_by(doNumber=doNumber).one_or_none()

    if doData is None:
        return None
    
    db.delete(doData)
    db.commit()

    return True

def deleteDONumberLogs(doNumber:str,db:Session,actionByUsername:str) -> bool:
    deleteDONumberLog= DoLog(
        doNumber=doNumber,
        action=ActionsTypeEnum.DELETED.value,
        actionBy=actionByUsername,
    )

    db.add(deleteDONumberLog)
    db.commit()
    db.refresh(deleteDONumberLog)

    if(deleteDONumberLog):
        return True
    
    return False