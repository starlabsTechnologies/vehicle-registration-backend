from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.models.doMaintenanceBase import DONumberResponse, CreateDONumber, UpdateDONumber
from app.services.doMaintenance.doMaintenanceServices import getDoDataByDoNumber,createDONumber,deleteDONumber,updateDONumber

def getDoDataController(doNumber:str,db:Session) -> DONumberResponse:
    doData=getDoDataByDoNumber(doNumber,db)

    if doData is None:
        return JSONResponse(
            content={"message": "Do Number not found"},
            status_code=404
        )
    
    return doData


def createDoNumberController(doInfo:CreateDONumber,db:Session) -> JSONResponse:
    if(not doInfo.doNumber or not doInfo.transporter or not doInfo.weighbridgeNo or not doInfo.validityTill or not doInfo.allotedQty or not doInfo.releasedQty ):
        return JSONResponse(
            content={"message": "Please Enter required fields"},
            status_code=400
        )
    
    if(len(doInfo.mobileNumber)!=10 and len(doInfo.mobileNumber)!=0):
        return JSONResponse(
            content={"message": "Mobile Number should be 10 digits exactly!"},
            status_code=400
        )
    
    doData=getDoDataByDoNumber(doInfo.doNumber,db)

    if doData is not None:
        return JSONResponse(
            content={"message": f"Do Number {doInfo.doNumber} already exists"},
            status_code=400
        )
    
    newDoData=createDONumber(doInfo,db)

    if not newDoData:
        return JSONResponse(
            content={"message": "Error creating new DO Number"},
            status_code=404
        )

    return JSONResponse(
        content={"message": "Do Number created successfully"},
        status_code=201
    )

def updateDONumberController(doInfo:UpdateDONumber,db:Session) -> JSONResponse:
    if not doInfo.doNumber:
        return JSONResponse(
            content={"message": "Please Enter doNumber"},
            status_code=400
        )
    
    success=updateDONumber(doInfo,db)
    
    if(success):
        return JSONResponse(
            content={"message": "DO Number updated successfully"},
            status_code=200
        )

    return JSONResponse(
        content={"message": "Error updating DO Number"},
        status_code=400
    ) 

def deleteDONumberController(doNumber:str,db:Session) -> JSONResponse:
    if not doNumber:
        return JSONResponse(
            content={"message": "Please Enter doInfo"},
            status_code=400
        )
    
    success=deleteDONumber(doNumber,db)

    if success is None:
        return JSONResponse(
            content={"message": "DO Number not found"},
            status_code=404
        )

    if(success):
        return JSONResponse(
            content={"message": "DO Number deleted successfully"},
            status_code=200
        )
    
    return JSONResponse(
        content={"message": "Error deleting DO Number"},
        status_code=400
    ) 