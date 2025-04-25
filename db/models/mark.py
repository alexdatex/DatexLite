from sqlalchemy import Column, Integer, String, Text, Boolean

from ..database import Base


class Mark(Base):
    __tablename__ = "mark"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    schema_id = Column(Integer, nullable=True, index=True)
    spare_parts = Column(Boolean)
    x = Column(Integer, nullable=False, index=True)
    y = Column(Integer, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    is_deleted = Column(Boolean, nullable=False, index=True, default=0)
