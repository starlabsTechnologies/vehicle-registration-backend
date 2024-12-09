from sqlalchemy.orm import Session
from app.schema.doMaintenance import DoData
from app.models.doMaintenanceBase import CreateDONumber,DONumberResponse, UpdateDONumber

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

def deleteDONumber(doNumber:str,db:Session) -> bool:
    doData=db.query(DoData).filter_by(doNumber=doNumber).one_or_none()

    if doData is None:
        return None
    
    db.delete(doData)
    db.commit()

    return True