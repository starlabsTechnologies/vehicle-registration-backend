from fastapi import APIRouter,Depends
from app.config.db_config import get_db
from sqlalchemy.orm import Session
from app.models.allotedTagsBase import DueAmount
from app.controllers.dueAmount.dueAmountController import currentDueAmountController

dueAmount_router=APIRouter()

@dueAmount_router.get("/due-amount",response_model=DueAmount)
def getDueAmount(db: Session = Depends(get_db)):
    return currentDueAmountController(db)