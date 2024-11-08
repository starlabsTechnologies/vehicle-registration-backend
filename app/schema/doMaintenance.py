from sqlalchemy import Column, String, Enum, Integer, DateTime, Text, Float
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum, BINARY as MySQLBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
import uuid

from app.config.db_config import Base


# Step 2: Define the Model
class DoData(Base):
    __tablename__ = "do_data"

    id = Column(MySQLBinary(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    doNumber = Column(String(255), nullable=False)
    weighbridgeNo = Column(Text, nullable=False)
    transporter = Column(Text, nullable=False)
    permissidoNameon = Column(Text, nullable=True)
    validThrough = Column(Text, nullable=True)
    validityTill = Column(Text, nullable=True)
    allotedQty = Column(Float, nullable=True)
    releasedQty = Column(Float, nullable=True)  # Released Quantity field
    leftQty = Column(Float, nullable=True)      # Left Quantity field
    doAddress = Column(Text, nullable=True)
    doRoute = Column(Text, nullable=True)
    salesOrder = Column(Text, nullable=True)
    customerId = Column(Text, nullable=True)
    mobileNumber = Column(Text, nullable=True)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(DoData, self).__init__(**kwargs)
        if isinstance(self.id, uuid.UUID):
            self.id = self.id.bytes
