from sqlalchemy import Column, Integer, String, LargeBinary, Text, Boolean

from ..database import Base


class MarkImage(Base):
    __tablename__ = "mark_image"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    data = Column(LargeBinary)
    mark_id = Column(Integer, nullable=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    is_deleted = Column(Boolean, nullable=False, index=True, default=0)
