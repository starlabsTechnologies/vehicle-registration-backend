from sqlalchemy import Column, String, Enum, Integer, DateTime, Text
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum, BINARY as MySQLBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
import uuid

from app.config.db_config import Base

class ActionsTypeEnum(PyEnum):  # Using Python's Enum class
    DELETED = "DELETED"
    CREATED = "CREATED"
    EDITED = "EDITED"

# Step 2: Define the Model
class UserInfoLogs(Base):
    __tablename__ = "user_info_logs"
    id = Column(MySQLBinary(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    username = Column(String(255), nullable=False)
    action = Column(Enum(ActionsTypeEnum), nullable=False)
    actionBy = Column(String(100), nullable=False)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(UserInfoLogs, self).__init__(**kwargs)
        if isinstance(self.id, uuid.UUID):
            self.id = self.id.bytes
