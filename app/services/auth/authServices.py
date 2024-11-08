from sqlalchemy.orm import Session
from app.schema.userInfo import UserInfo
from app.models.userInfoBase import UserInfoResponse,CreateUser
import bcrypt
from typing import Optional, Union

def getUserByUserName(username:str,db:Session) -> Optional[UserInfoResponse]:
    user = db.query(UserInfo).filter_by(username=username).one_or_none()

    if user is None:
        return None

    return UserInfoResponse(
        id=str(user.id),
        username=user.username,
        password=user.password,
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
    user=getUserByUserName(username,db)

    if user is None:
        return None
    
    bytes_password = password.encode('utf-8')
    hashed_password = user.password.encode('utf-8')
    result=bcrypt.checkpw(bytes_password,hashed_password)

    if result:
        return user
    
    return False

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

def deleteUserByUsername(username:str,db:Session) -> bool:
    user = db.query(UserInfo).filter_by(username=username).one_or_none()

    if user is None:
        return None
    
    db.delete(user)
    db.commit()

    return True