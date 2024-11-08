from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.models.doMaintenanceBase import DONumberResponse, CreateDONumber
from app.services.doMaintenance.doMaintenanceServices import getDoDataByDoNumber,createDONumber,deleteDONumber

def getDoDataController(doNumber:str,db:Session) -> DONumberResponse:
    doData=getDoDataByDoNumber(doNumber,db)

    if doData is None:
        return JSONResponse(
            content={"message": "Do Number not found"},
            status_code=404
        )
    
    return doData


def createDoNumberController(doInfo:CreateDONumber,db:Session) -> JSONResponse:
    if(not doInfo.doNumber or not doInfo.transporter):
        return JSONResponse(
            content={"message": "Please Enter DoNumber and Transporter"},
            status_code=400
        )
    
    if(len(doInfo.mobileNumber)!=10):
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

def deleteDONumberController(doNumber:str,db:Session) -> JSONResponse:
    if not doNumber:
        return JSONResponse(
            content={"message": "Please Enter Username"},
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