from app.config.db_config import SessionLocal
from app.schema.userInfo import UserInfo, AuthTypeEnum
import bcrypt
import os

def automate_saving_master_user():
    try:
        db=SessionLocal()

        password=os.getenv("MASTER_USER_PASSWORD")
        bytes_password = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=10)
        hashedpassword=bcrypt.hashpw(bytes_password,salt)

        existing_user = db.query(UserInfo).filter_by(
            username="SLT_W",  # In production, use hashed passwords for security!
            authType=AuthTypeEnum.MASTER
        ).one_or_none()

        if (existing_user and not bcrypt.checkpw(password.encode('utf-8'), existing_user.password.encode('utf-8'))):
            existing_user=None

        if existing_user is None:
            # If the user doesn't exist, insert the new master user
            master_user = UserInfo(
                username="SLT_W",
                password=hashedpassword,  # It's recommended to hash the password in a real application
                authType=AuthTypeEnum.MASTER,
                empId=None,
                fullName="VAIBHAV",
                email=None,
                desigantion=None,
                Address=None,
                mobileNumber=None,
                organisation=None,
            )

            db.add(master_user)
            db.commit()

            print("Master user inserted successfully.")
        else:
            print("Master user with the same credentials already exists. Skipping insertion.")

    except Exception as e:
        print(f"An error occurred while checking/inserting the master user: {e}")