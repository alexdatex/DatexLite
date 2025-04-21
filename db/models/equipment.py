from sqlalchemy import Column, Integer, String,Date
from ..database import Base

class Equipment(Base):
    __tablename__ = "equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    code = Column(String, unique=True, index=True)
    purpose = Column(String, unique=False, index=True)
    manufacturer = Column(String(100), nullable=True)
    type = Column(String(100), nullable=True)
    serial_number = Column(String(50), unique=False, nullable=True)
    production_date = Column(Date, nullable=True)
    location = Column(String(100), nullable=True)
