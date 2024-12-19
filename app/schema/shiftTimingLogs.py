from sqlalchemy import Column, String, Time, DateTime, Enum
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum, BINARY as MySQLBinary
from datetime import datetime
from enum import Enum as PyEnum
import uuid
from app.config.db_config import Base

class ActionsTypeEnum(PyEnum):  # Using Python's Enum class
    DELETED = "DELETED"
    CREATED = "CREATED"
    EDITED = "EDITED"

# Step 2: Define the Model
class ShiftTimingLogs(Base):
    __tablename__ = "shift_timing_logs"

    id = Column(MySQLBinary(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    shift_name = Column(String(50), nullable=False)
    from_time = Column(Time, nullable=False)
    to_time = Column(Time, nullable=False)
    action = Column(Enum(ActionsTypeEnum), nullable=False)
    actionBy = Column(String(100), nullable=False)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(ShiftTimingLogs, self).__init__(**kwargs)
        if isinstance(self.id, uuid.UUID):
            self.id = self.id.bytes
