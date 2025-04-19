from sqlalchemy import Column, Integer, String, Date, LargeBinary
from ..database import Base


class MarkImage(Base):
    __tablename__ = "mask_image"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    data = Column(LargeBinary)
    mark_id = Column(Integer, nullable=True, index=True)
