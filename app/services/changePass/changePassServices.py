from sqlalchemy.orm import Session
from app.schema.userInfo import UserInfo
from app.models.userInfoBase import EditUser
import bcrypt

def editUser(userInfo:EditUser,db:Session) -> bool:
    user = db.query(UserInfo).filter_by(username=userInfo.username).one_or_none()

    if user is None:
        return None

    bytes_password = userInfo.password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=10)
    hashedpassword=bcrypt.hashpw(bytes_password,salt)

    
    user.username = userInfo.username,
    user.password=hashedpassword,
    user.fullName=userInfo.fullName,
    user.email=userInfo.email,
    user.Address=userInfo.Address,
    user.mobileNumber=userInfo.mobileNumber,

    db.commit()
    db.refresh(user)

    return True