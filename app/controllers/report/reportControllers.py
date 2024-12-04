from app.models.vehicleInOutBase import VehicleInOutResponse,SummaryFilter,WeighbridgeWiseFilter,ShiftWiseFilter,DoWiseFilter,VehicleTypeFilter,ValidityWiseFilter,DataFilter,OptionsEnum
from app.services.report.reportServices import getSummary,getWeighbridgeWise,getShiftWise,getDoWise,getVehicleType,getValidityWise,getRegistrationDetails,getVehicleInOutData
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.models.vehicleRegistrationBase import RegistrationDetailsResponse
from typing import List, Union
from app.utils.logger import logger

def setOptionController(filterInfo:DataFilter,db:Session) -> List[Union[VehicleInOutResponse, RegistrationDetailsResponse]]:
    try:
        if(filterInfo.option == OptionsEnum.Summary):
            filter=SummaryFilter(
                dateIn=filterInfo.dateIn,
                dateOut=filterInfo.dateOut,
                timeIn=filterInfo.timeIn,
                timeOut=filterInfo.timeOut
            )

            return getSummaryController(filter,db)
        
        elif(filterInfo.option == OptionsEnum.WeighbridgeWise):
            filter=WeighbridgeWiseFilter(
                dateIn=filterInfo.dateIn,
                dateOut=filterInfo.dateOut,
                timeIn=filterInfo.timeIn,
                timeOut=filterInfo.timeOut,
            )

            return getWeighbridgeWiseController(filter,db)
        
        elif(filterInfo.option == OptionsEnum.ShiftWise):
            filter=ShiftWiseFilter(
                dateIn=filterInfo.dateIn,
                dateOut=filterInfo.dateOut,
            )

            return getShiftWiseController(filter,db)
        
        elif(filterInfo.option == OptionsEnum.DoWise):
            filter=DoWiseFilter(
                dateIn=filterInfo.dateIn,
                dateOut=filterInfo.dateOut,
                timeIn=filterInfo.timeIn,
                timeOut=filterInfo.timeOut,
            )

            return getDoWiseController(filter,db)
        
        elif(filterInfo.option == OptionsEnum.VehicleType):
            filter=VehicleTypeFilter(
                dateIn=filterInfo.dateIn,
                dateOut=filterInfo.dateOut,
                timeIn=filterInfo.timeIn,
                timeOut=filterInfo.timeOut,
            )

            return getVehicleTypeController(filter,db)
        
        elif(filterInfo.option == OptionsEnum.ValidityWise):
            filter=ValidityWiseFilter(
                dateIn=filterInfo.dateIn,
                dateOut=filterInfo.dateOut,
                timeIn=filterInfo.timeIn,
                timeOut=filterInfo.timeOut,
            )

            return getValidityWiseController(filter,db)
        
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

def getSummaryController(filterInfo:SummaryFilter,db:Session) -> List[VehicleInOutResponse]:
    try:
        result=getSummary(filterInfo,db)

        if (len(result) == 0):
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
    
def getWeighbridgeWiseController(filterInfo:WeighbridgeWiseFilter,db:Session) -> List[VehicleInOutResponse]:
    try:
        result=getWeighbridgeWise(filterInfo,db)

        if (len(result) == 0):
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
    
def getShiftWiseController(filterInfo:ShiftWiseFilter,db:Session) -> List[VehicleInOutResponse]:
    try:
        result=getShiftWise(filterInfo,db)

        if (len(result) == 0):
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
    
def getDoWiseController(filterInfo:DoWiseFilter,db:Session) -> List[VehicleInOutResponse]:
    try:
        result=getDoWise(filterInfo,db)

        if (len(result) == 0):
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
    
def getVehicleTypeController(filterInfo:VehicleTypeFilter,db:Session) -> List[VehicleInOutResponse]:
    try:
        result=getVehicleType(filterInfo,db)

        if (len(result) == 0):
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
    
def getValidityWiseController(filterInfo:ValidityWiseFilter,db:Session) -> List[VehicleInOutResponse]:
    try:
        result=getValidityWise(filterInfo,db)

        if (len(result) == 0):
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
    
def getRegistrationDetailsController(db:Session) -> List[RegistrationDetailsResponse]:
    try:
        result=getRegistrationDetails(db)

        if (len(result) == 0):
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