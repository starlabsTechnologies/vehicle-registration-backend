from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schema.allotedTags import AllotedTags
from app.schema.allotedTagsLogs import AllotedTagsLogs
from enum import Enum

class ActionsTypeEnum(Enum):  # Using Python's Enum class
    DELETED = "DELETED"
    CREATED = "CREATED"
    EDITED = "EDITED"

def changeBlacklistStatus(rfidTag:str,vehicleNo:str,action:str,db:Session) -> bool:
    userInfo=db.query(AllotedTags).filter(or_(AllotedTags.rfidTag==rfidTag,AllotedTags.vehicleNumber==vehicleNo)).first()

    if userInfo is None:
        return None
    
    if action == 'Blacklist':
        desired_status=True
    elif action == 'Unblacklist':
        desired_status=False
    
    if userInfo.blacklisted == desired_status:
        return False
    
    userInfo.blacklisted=desired_status
    db.commit()

    return True

def changeBlackListStatusLogs(rfidTag:str,vehicleNo:str,action:str,actionByUsername:str,db:Session) -> bool:
    if action == 'Blacklist':
        desired_status=True
    elif action == 'Unblacklist':
        desired_status=False

    changeBlackListLog= AllotedTagsLogs(
        rfidTag=rfidTag,
        vehicleNumber=vehicleNo,
        blackListAction=desired_status,
        action=ActionsTypeEnum.EDITED.value,
        actionBy=actionByUsername,
    )

    db.add(changeBlackListLog)
    db.commit()
    db.refresh(changeBlackListLog)

    if(changeBlackListLog):
        return True
    
    return False