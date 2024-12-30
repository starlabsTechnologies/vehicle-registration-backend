from app.services.dueAmount.dueAmountServices import dueAmount
from app.models.allotedTagsBase import DueAmount
from sqlalchemy.orm import Session
from app.utils.logger import logger
from fastapi.responses import JSONResponse

def currentDueAmountController(db:Session) -> DueAmount:
    try:
        due = dueAmount(db)

        if not due:
            logger.warning("Due Amount Not Found")
            return JSONResponse(
                    content={"message": "Due Amount Not Found"},
                    status_code=404
                )
        
        logger.info("Due Amount fetched successfully")
        return due
    
    except Exception as error:
        logger.error(f"Error occurred while fetching Due Amount: {error}")
        return JSONResponse(
            content={"message": "Error occurred while fetching Due Amount"},
            status_code=500
        )
    