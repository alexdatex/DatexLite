from sqlalchemy import Column, Integer, String, Date, LargeBinary
from ..database import Base


class Mark(Base):
    __tablename__ = "mask"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    schema_id = Column(Integer, nullable=True, index=True)
    x = Column(Integer, nullable=False, index=True)
    y = Column(Integer, nullable=False, index=True)
