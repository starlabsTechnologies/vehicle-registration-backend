from app.services.internalRfid.internalRfidServices import getVehicleReg,createVehicleReg,editVehicleReg,deleteVehicleReg
from app.models.vehicleRegistrationBase import VehicleRegistrationResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,SuccessResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

def getVehicleRegController(rfidTag:str,db:Session) -> VehicleRegistrationResponse:
    vehicleReg=getVehicleReg(rfidTag,db)

    if vehicleReg is None:
        return JSONResponse(
            content={"message":"Vehicle Registration not found."},
            status_code=404
        )
    
    return vehicleReg

def createVehicleRegController(vehicleInfo:CreateVehicleRegistration,db:Session) -> SuccessResponse:
    if not vehicleInfo.rfidTag:
        return JSONResponse(
            content={"message":"Rfid Tag required"},
            status_code=400
        )

    vehicleReg=getVehicleReg(vehicleInfo.rfidTag,db)

    if vehicleReg is not None:
        return JSONResponse(
            content={"message": "Vehicle with Rfid Tag already exists"},
            status_code=400
        )
    
    newReg=createVehicleReg(vehicleInfo,db)

    if not newReg:
        return JSONResponse(
            content={"message":"Error occurred registering vehicle"},
            status_code=400
        )
    
    return SuccessResponse(
        message="Vehicle Registered successfully"
    )


def editVehicleRegController(vehicleInfo:EditVehicleRegistration,db:Session) -> SuccessResponse:
    if not vehicleInfo.rfidTag:
        return JSONResponse(
            content={"message":"Rfid Tag required"},
            status_code=400
        )
    
    edited=editVehicleReg(vehicleInfo,db)

    if edited is None:
        return JSONResponse(
            content={"message":"Vehicle Registration not found."},
            status_code=404
        )
    
    return SuccessResponse(
        message="Vehicle Registration updated successfully"
    )

def deleteVehicleRegController(vehicleInfo:DeleteVehicleRegistration,db:Session) -> SuccessResponse:
    if not vehicleInfo.rfidTag:
        return JSONResponse(
            content={"message":"Rfid Tag required"},
            status_code=400
        )
    
    success=deleteVehicleReg(vehicleInfo,db)

    if success is None:
        return JSONResponse(
            content={"message":"Vehicle Registration not found."},
            status_code=404
        )
    
    if not success:
        return JSONResponse(
            content={"message": "Error deleting data"},
            status_code=400
        )
    
    return SuccessResponse(
        message="Data has been deleted successfully"
    )