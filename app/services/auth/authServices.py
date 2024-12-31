from sqlalchemy.orm import Session
from app.schema.userInfo import UserInfo, AuthTypeEnum, ActiveStatusTypeEnum
from app.schema.userInfoLogs import UserInfoLogs
from app.models.userInfoBase import UserInfoResponse,CreateUser
import bcrypt
from enum import Enum
from typing import Optional, Union

class AuthResult(Enum):
    USER_NOT_FOUND = "User not found"
    INCORRECT_PASSWORD = "Incorrect password"
    UNAUTHORIZED_ACCESS = "Unauthorized access"
    AUTHORIZED = "Authorized"

class ActionsTypeEnum(Enum):  # Using Python's Enum class
    DELETED = "DELETED"
    CREATED = "CREATED"
    EDITED = "EDITED"

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

def getUserByUserName(username:str,db:Session) -> Optional[UserInfoResponse]:
    user = db.query(UserInfo).filter_by(username=username).one_or_none()

    if user is None:
        return None

    return UserInfoResponse(
        id=str(user.id),
        username=user.username,
        authType=user.authType,
        empId=user.empId,
        fullName=user.fullName,
        email=user.email,
        desigantion=user.desigantion,
        Address=user.Address,
        mobileNumber=user.mobileNumber,
        organisation=user.organisation,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt
    )

def logUserIn(username:str,password:str,db:Session) -> Union[UserInfoResponse, bool, None]:
    user = getUserByUserName(username,db)
    db_user=db.query(UserInfo).filter_by(username=username).one_or_none()

    if user is None:
        return None
    
    bytes_password = password.encode('utf-8')
    hashed_password = db_user.password.encode('utf-8')
    result=bcrypt.checkpw(bytes_password,hashed_password)

    if result:
        db_user.status = ActiveStatusTypeEnum.ACTIVE.name
        db.commit()
        db.refresh(db_user)
        return user
    
    return False

def logUserOut(username:str,db:Session) -> bool:
    user=db.query(UserInfo).filter_by(username=username).one_or_none()

    if user is None:
        return None
    
    user.status = ActiveStatusTypeEnum.LOGOUT.name
    db.commit()
    db.refresh(user)

    return True

def createUser(userInfo: CreateUser,db:Session) -> bool: 
    bytes_password = userInfo.password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=10)
    hashedpassword=bcrypt.hashpw(bytes_password,salt)

    newUser=UserInfo(
        username=userInfo.username,
        password=hashedpassword,
        authType=userInfo.authType,
        empId=userInfo.empId,
        fullName=userInfo.fullName,
        email=userInfo.email,
        desigantion=userInfo.desigantion,
        Address=userInfo.Address,
        mobileNumber=userInfo.mobileNumber,
        organisation=userInfo.organisation
    )

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    if(newUser):
        return True
    
    return False

def logCreateUser(username: str,db:Session,actionByUsername:str) -> bool:
    print(username,ActionsTypeEnum.CREATED,actionByUsername)
    logNewUser= UserInfoLogs(
        username=username,
        action=ActionsTypeEnum.CREATED.value,
        actionBy=actionByUsername,
    )

    db.add(logNewUser)
    db.commit()
    db.refresh(logNewUser)

    if(logNewUser):
        return True
    
    return False

def deleteUserByUsername(username:str,db:Session) -> bool:
    user = db.query(UserInfo).filter_by(username=username).one_or_none()

    if user is None:
        return None
    
    db.delete(user)
    db.commit()

    return True

def logDeleteUser(username: str,db:Session,actionByUsername:str) -> bool:
    logDelUser= UserInfoLogs(
        username=username,
        action=ActionsTypeEnum.DELETED.value,
        actionBy=actionByUsername,
    )

    db.add(logDelUser)
    db.commit()
    db.refresh(logDelUser)

    if(logDelUser):
        return True
    
    return False