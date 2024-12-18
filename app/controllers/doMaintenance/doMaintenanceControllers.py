from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.models.doMaintenanceBase import DONumberResponse, CreateDONumber, UpdateDONumber
from app.services.doMaintenance.doMaintenanceServices import getDoDataByDoNumber,createDONumber,deleteDONumber,updateDONumber,createDONumberLogs,updateDONumberLogs,deleteDONumberLogs

def getDoDataController(doNumber:str,db:Session) -> DONumberResponse:
    try:
        doData=getDoDataByDoNumber(doNumber,db)

        if doData is None:
            logger.warning(f"Do Number not found: {doNumber}")
            return JSONResponse(
                content={"message": "Do Number not found"},
                status_code=404
            )
        
        logger.info(f"Do Number {doNumber} fetched successfully")
        return doData
    
    except Exception as error:
        logger.error(f"Error occurred while fetching do Number: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching do Number"},
            status_code=500
        )


def createDoNumberController(req:Request,doInfo:CreateDONumber,db:Session) -> JSONResponse:
    try:
        headers = req.headers
        authorization = headers.get("authorization")
        if not authorization:
            logger.warning("Authorization header missing")
            return JSONResponse(
                content={"message": "Authorization header missing"},
                status_code=400
            )
        
        actionByUsername = authorization

        if(not doInfo.doNumber or not doInfo.transporter or not doInfo.weighbridgeNo or not doInfo.validityTill or not doInfo.allotedQty or not doInfo.releasedQty ):
            logger.warning("Please Enter required fields")
            return JSONResponse(
                content={"message": "Please Enter required fields"},
                status_code=400
            )
        
        if(len(doInfo.mobileNumber)!=10 and len(doInfo.mobileNumber)!=0):
            logger.warning("Mobile Number should be 10 digits exactly!")
            return JSONResponse(
                content={"message": "Mobile Number should be 10 digits exactly!"},
                status_code=400
            )
        
        doData=getDoDataByDoNumber(doInfo.doNumber,db)

        if doData is not None:
            logger.warning(f"Do Number {doInfo.doNumber} already exists")
            return JSONResponse(
                content={"message": f"Do Number {doInfo.doNumber} already exists"},
                status_code=400
            )
        
        newDoData=createDONumber(doInfo,db)

        if not newDoData:
            logger.warning("Error creating new DO Number")
            return JSONResponse(
                content={"message": "Error creating new DO Number"},
                status_code=404
            )

        logger.info(f"Do Number {doInfo.doNumber} created successfully")

        createDONumberLog = createDONumberLogs(doInfo,db,actionByUsername)
        if(createDONumberLog):
            logger.info("DO Number creation logged successfully")
        else:
            logger.info("Logging of DO Number creation unsuccessful")

        return JSONResponse(
            content={"message": "Do Number created successfully"},
            status_code=201
        )
    
    except Exception as error:
        logger.error(f"Error occurred while creating DO Number: {error}")
        return JSONResponse(
            content={"message": "Error occurred while creating DO Number"},
            status_code=500
        )

def updateDONumberController(req:Request,doInfo:UpdateDONumber,db:Session) -> JSONResponse:
    try:
        headers = req.headers
        authorization = headers.get("authorization")
        if not authorization:
            logger.warning("Authorization header missing")
            return JSONResponse(
                content={"message": "Authorization header missing"},
                status_code=400
            )
        
        actionByUsername = authorization

        if not doInfo.doNumber:
            logger.warning("Please Enter doNumber")
            return JSONResponse(
                content={"message": "Please Enter doNumber"},
                status_code=400
            )
        
        success=updateDONumber(doInfo,db)
        
        if(success):
            logger.info(f"DO Number {doInfo.doNumber} updated successfully")

            updateDONumberLog = updateDONumberLogs(doInfo,db,actionByUsername)
            if(updateDONumberLog):
                logger.info("DO Number edit logged successfully")
            else:
                logger.info("Logging of DO Number edit unsuccessful")

            return JSONResponse(
                content={"message": "DO Number updated successfully"},
                status_code=200
            )

        logger.warning(f"Error updating DO Number: {doInfo.doNumber}")
        return JSONResponse(
            content={"message": "Error updating DO Number"},
            status_code=400
        )
    
    except Exception as error:
        logger.error(f"Error occurred while updating do Number: {error}")
        return JSONResponse(
            content={"message": "Error occurred while updating do Number"},
            status_code=500
        )

def deleteDONumberController(req:Request,doNumber:str,db:Session) -> JSONResponse:
    try:
        headers = req.headers
        authorization = headers.get("authorization")
        if not authorization:
            logger.warning("Authorization header missing")
            return JSONResponse(
                content={"message": "Authorization header missing"},
                status_code=400
            )
        
        actionByUsername = authorization

        if not doNumber:
            logger.warning("Please Enter doInfo")
            return JSONResponse(
                content={"message": "Please Enter doInfo"},
                status_code=400
            )
        
        success=deleteDONumber(doNumber,db)

        if success is None:
            logger.warning(f"Do Number not found: {doNumber}")
            return JSONResponse(
                content={"message": "DO Number not found"},
                status_code=404
            )

        if(success):
            logger.info(f"DO Number {doNumber} deleted successfully")

            delDONumberLog = deleteDONumberLogs(doNumber,db,actionByUsername)
            if(delDONumberLog):
                logger.info("DO Number delete logged successfully")
            else:
                logger.info("Logging of DO Number delete unsuccessful")
                
            return JSONResponse(
                content={"message": "DO Number deleted successfully"},
                status_code=200
            )
        
        logger.warning(f"Error deleting DO Number: {doNumber}")        
        return JSONResponse(
            content={"message": "Error deleting DO Number"},
            status_code=400
        )
    
    except Exception as error:
        logger.error(f"Error occurred while deleting DO Number: {error}")
        return JSONResponse(
            content={"message": "Error occurred while deleting DO Number"},
            status_code=500
        )