from app.models.vehicleInOutBase import VehicleInOutResponse,SummaryFilter,WeighbridgeWiseFilter,ShiftWiseFilter,DoWiseFilter,VehicleTypeFilter,ValidityWiseFilter,OptionsEnum,PaginatedVehicleInOutResponse
from app.services.report.reportServices import getSummary,getWeighbridgeWise,getShiftWise,getDoWise,getVehicleType,getValidityWise,getRegistrationDetails,getVehicleInOutData
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.models.vehicleRegistrationBase import PaginatedRegResponse
from typing import List, Union, Optional
from fastapi import Query
from app.utils.logger import logger

def setOptionController(db:Session,option: OptionsEnum = Query(None),dateIn: Optional[str] = Query(None),dateOut: Optional[str] = Query(None),timeIn: Optional[str] = Query(None),timeOut: Optional[str] = Query(None),page: int = Query(1, ge=1),pageSize: int = Query(10, ge=1, le=100)) -> Union[PaginatedVehicleInOutResponse, PaginatedRegResponse]:
    try:
        if(option == OptionsEnum.Summary):
            filter=SummaryFilter(
                dateIn=dateIn,
                dateOut=dateOut,
                timeIn=timeIn,
                timeOut=timeOut
            )

            return getSummaryController(filter,db,page,pageSize)
        
        elif(option == OptionsEnum.WeighbridgeWise):
            filter=WeighbridgeWiseFilter(
                dateIn=dateIn,
                dateOut=dateOut,
                timeIn=timeIn,
                timeOut=timeOut,
            )

            return getWeighbridgeWiseController(filter,db,page,pageSize)
        
        elif(option == OptionsEnum.ShiftWise):
            filter=ShiftWiseFilter(
                dateIn=dateIn,
                dateOut=dateOut,
            )

            return getShiftWiseController(filter,db,page,pageSize)
        
        elif(option == OptionsEnum.DoWise):
            filter=DoWiseFilter(
                dateIn=dateIn,
                dateOut=dateOut,
                timeIn=timeIn,
                timeOut=timeOut,
            )

            return getDoWiseController(filter,db,page,pageSize)
        
        elif(option == OptionsEnum.VehicleType):
            filter=VehicleTypeFilter(
                dateIn=dateIn,
                dateOut=dateOut,
                timeIn=timeIn,
                timeOut=timeOut,
            )

            return getVehicleTypeController(filter,db,page,pageSize)
        
        elif(option == OptionsEnum.ValidityWise):
            filter=ValidityWiseFilter(
                dateIn=dateIn,
                dateOut=dateOut,
                timeIn=timeIn,
                timeOut=timeOut,
            )

            return getValidityWiseController(filter,db,page,pageSize)
        
        else:
            logger.warning("Wrong option Entered")
            return JSONResponse(
                content={"message": "Wrong option Entered"},
                status_code=400
            )

    except Exception as error:
        logger.error(f"Error occurred while fetching Options data: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching Options data"},
            status_code=500
        )

def getSummaryController(filterInfo:SummaryFilter,db:Session,page: int =1,pageSize: int=1) -> PaginatedVehicleInOutResponse:
    try:
        result=getSummary(filterInfo,db,page,pageSize)

        if (len(result.data) == 0):
            logger.warning("No data found")
            return JSONResponse(
                content={"message":"No data found"},
                status_code=404
            )

        logger.info("Summary data fetched successfully")
        return result
    
    except Exception as error:
        logger.error(f"Error occurred while fetching Summary data: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching Summary data"},
            status_code=500
        )
    
def getWeighbridgeWiseController(filterInfo:WeighbridgeWiseFilter,db:Session,page: int =1,pageSize: int=1) -> PaginatedVehicleInOutResponse:
    try:
        result=getWeighbridgeWise(filterInfo,db,page,pageSize)

        if (len(result.data) == 0):
            logger.warning("No data found")
            return JSONResponse(
                content={"message":"No data found"},
                status_code=404
            )
        
        logger.info("Weighbridge Wise data fetched successfully")
        return result
    
    except Exception as error:
        logger.error(f"Error occurred while fetching Weighbridge Wise data: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching Weighbridge Wise data"},
            status_code=500
        )
    
def getShiftWiseController(filterInfo:ShiftWiseFilter,db:Session,page: int =1,pageSize: int=1) -> PaginatedVehicleInOutResponse:
    try:
        result=getShiftWise(filterInfo,db,page,pageSize)

        if (len(result.data) == 0):
            logger.warning("No data found")
            return JSONResponse(
                content={"message":"No data found"},
                status_code=404
            )
        
        logger.info("Shift Wise data fetched successfully")
        return result
    
    except Exception as error:
        logger.error(f"Error occurred while fetching Shift Wise data: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching Shift Wise data"},
            status_code=500
        )
    
def getDoWiseController(filterInfo:DoWiseFilter,db:Session,page: int =1,pageSize: int=1) -> PaginatedVehicleInOutResponse:
    try:
        result=getDoWise(filterInfo,db,page,pageSize)

        if (len(result.data) == 0):
            logger.warning("No data found")
            return JSONResponse(
                content={"message":"No data found"},
                status_code=404
            )
        
        logger.info("Do Wise data fetched successfully")
        return result
    
    except Exception as error:
        logger.error(f"Error occurred while fetching Do Wise data: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching Do Wise data"},
            status_code=500
        )
    
def getVehicleTypeController(filterInfo:VehicleTypeFilter,db:Session,page: int =1,pageSize: int=1) -> PaginatedVehicleInOutResponse:
    try:
        result=getVehicleType(filterInfo,db,page,pageSize)

        if (len(result.data) == 0):
            logger.warning("No data found")
            return JSONResponse(
                content={"message":"No data found"},
                status_code=404
            )
        
        logger.info("Vehicle Type data fetched successfully")
        return result
    
    except Exception as error:
        logger.error(f"Error occurred while fetching Vehicle Type data: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching Vehicle Type data"},
            status_code=500
        )
    
def getValidityWiseController(filterInfo:ValidityWiseFilter,db:Session,page: int =1,pageSize: int=1) -> PaginatedVehicleInOutResponse:
    try:
        result=getValidityWise(filterInfo,db,page,pageSize)

        if (len(result.data) == 0):
            logger.warning("No data found")
            return JSONResponse(
                content={"message":"No data found"},
                status_code=404
            )
        
        logger.info("Validity Wise data fetched successfully")
        return result
    
    except Exception as error:
        logger.error(f"Error occurred while fetching Validity Wise data: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching Validity Wise data"},
            status_code=500
        )
    
def getVehicleInOutDataController(db:Session) -> List[VehicleInOutResponse]:
    try:
        result=getVehicleInOutData(db)

        if (len(result) == 0):
            logger.warning("No data found")
            return JSONResponse(
                content={"message":"No data found"},
                status_code=404
            )
        
        logger.info("Vehicle In Out data fetched successfully")
        return result
    
    except Exception as error:
        logger.error(f"Error occurred while fetching Vehicle In Out data: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching Vehicle In Out data"},
            status_code=500
        )
    
def getRegistrationDetailsController(db:Session,page: int =1,pageSize: int=1) -> PaginatedRegResponse:
    try:
        result=getRegistrationDetails(db,page,pageSize)

        if (len(result.data) == 0):
            logger.warning("No data found")
            return JSONResponse(
                content={"message":"No data found"},
                status_code=404
            )
        
        logger.info("Registration Details data fetched successfully")
        return result
    
    except Exception as error:
        logger.error(f"Error occurred while fetching Registration Details data: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching Registration Details data"},
            status_code=500
        )