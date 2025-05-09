from sqlalchemy import Column, Integer, String, LargeBinary, Boolean

from ..database import Base


class EquipmentSchema(Base):
    __tablename__ = "equipment_schema"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    data_image = Column(LargeBinary)
    data_original = Column(LargeBinary)
    equipment_id = Column(Integer, nullable=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    is_deleted = Column(Boolean, nullable=False, index=True, default=0)
