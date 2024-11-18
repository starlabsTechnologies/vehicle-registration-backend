from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schema.allotedTags import AllotedTags

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