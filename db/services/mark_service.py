from sqlalchemy.orm import Session

from ..models import EquipmentSchema
from ..models.equipment import Equipment
from ..models.mark import Mark


class MarkService:
    @staticmethod
    def get_mark(db: Session, mark_id: int):
        return db.query(Mark).filter(Mark.id == mark_id).first()

    @staticmethod
    def get_marks(db: Session, schema_id: int):
        return db.query(Mark).filter(Mark.schema_id == schema_id).all()
