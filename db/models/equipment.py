from sqlalchemy import Column, Integer, String,Date
from ..database import Base

class Equipment(Base):
    __tablename__ = "equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    code = Column(String, unique=True, index=True)
    purpose = Column(String, unique=True, index=True)
    description = Column(String, unique=True, index=True)
    serial_number = Column(String(50), unique=True, nullable=False)
    production_date = Column(Date, nullable=False)
    manufacturer = Column(String(100), nullable=False)
    location_id = Column(String(100), nullable=False)
    status = Column(String(100), nullable=False)