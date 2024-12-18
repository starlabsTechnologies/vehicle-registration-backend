from sqlalchemy import Column, String, Enum, Integer, DateTime, Text,Boolean
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum, BINARY as MySQLBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
import uuid

from app.config.db_config import Base

class VehicleTypeEnum(PyEnum):  # Using Python's Enum class
    TCT = "TCT"
    PDV = "PDV"
    TVV = "TVV"
    TOV = "TOV"
    PCT = "PCT"
    TDBEV = "TDBEV"
    SCRAPE = "SCRAPE"

class ActionsTypeEnum(PyEnum):  # Using Python's Enum class
    DELETED = "DELETED"
    CREATED = "CREATED"
    EDITED = "EDITED"
    BLACKLISTED = "BLACKLISTED"
    UNBLACKLISTED = "UNBLACKLISTED"

# Step 2: Define the Model
class AllotedTagsLogs(Base):
    __tablename__ = "alloted_tags_logs"

    id = Column(MySQLBinary(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    rfidTag = Column(String(255), nullable=False)
    vehicleNumber = Column(String(100), nullable=False)
    blackListAction = Column(Boolean, default=False, nullable=True)
    typeOfVehicle = Column(Enum(VehicleTypeEnum), nullable=True)
    action = Column(MySQLEnum(ActionsTypeEnum), nullable=False)
    actionBy = Column(String(100), nullable=False)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(AllotedTagsLogs, self).__init__(**kwargs)
        if isinstance(self.id, uuid.UUID):
            self.id = self.id.bytes
