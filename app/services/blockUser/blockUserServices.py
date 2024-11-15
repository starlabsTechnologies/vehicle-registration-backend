from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schema.userInfo import UserInfo,AuthTypeEnum
from app.schema.allotedTags import AllotedTags
import bcrypt
from enum import Enum
from typing import Optional, Union

class AuthResult(Enum):
    USER_NOT_FOUND = "User not found"
    INCORRECT_PASSWORD = "Incorrect password"
    UNAUTHORIZED_ACCESS = "Unauthorized access"
    AUTHORIZED = "Authorized"

def authorizeUser(username:str,password:str,db:Session) -> AuthResult:
    user=db.query(UserInfo).filter_by(username=username).one_or_none()

    if user is None:
        return AuthResult.USER_NOT_FOUND
    
    bytes_password = password.encode('utf-8')
    hashed_password = user.password.encode('utf-8')
    result=bcrypt.checkpw(bytes_password,hashed_password)

    if not result:
        return AuthResult.INCORRECT_PASSWORD
    
    isAuthorized=user.authType in [AuthTypeEnum.ADMIN,AuthTypeEnum.MASTER]

    if(isAuthorized):
        return AuthResult.AUTHORIZED
    
    return AuthResult.UNAUTHORIZED_ACCESS

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