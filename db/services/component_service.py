from sqlalchemy.orm import Session

from ..models import EquipmentSchema
from ..models.equipment import Equipment

class ComponentService:
    @staticmethod
    def get_component(db: Session, component_id: int):
        return db.query(Equipment).filter(Equipment.id == component_id).first()

    @staticmethod
    def get_components(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Equipment).offset(skip).limit(limit).all()

    @staticmethod
    def create_component(db: Session, name: str, description: str):
        db_component = Equipment(
            name=name,
            description=update_description
        )

        db.add(db_component)
        db.commit()
        db.refresh(db_component)
        return db_component

    @staticmethod
    def get_schemas(db: Session, equipment_id: int):
        return db.query(EquipmentSchema).filter(EquipmentSchema.equipment_id == equipment_id).all()
