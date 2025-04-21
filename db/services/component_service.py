from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ..models import EquipmentSchema
from ..models.equipment import Equipment


class ComponentService:
    @staticmethod
    def get_component(db: Session, component_id: int):
        return db.query(Equipment).filter(Equipment.id == component_id, Equipment.is_deleted == False).first()

    @staticmethod
    def get_components(db: Session, filters=None):
        if filters:
            conditions = [Equipment.is_deleted == False]
            for field in filters:
                if hasattr(Equipment, field):
                    value = filters[field].get().strip().replace('%', '\\%').replace('_', '\\_')
                    if value:
                        field = f"{field}_lower"
                        if hasattr(Equipment, field):
                            value=value.lower()
                            conditions.append(getattr(Equipment, field).like(f"%{value}%"))
            query = db.query(Equipment)
            if len(conditions) == 1:
                return query.filter(conditions[0])

            return query.filter(and_(*conditions))
        else:
            return db.query(Equipment).filter(Equipment.is_deleted == False).all()

    @staticmethod
    def get_schemas(db: Session, equipment_id: int):
        return db.query(EquipmentSchema).filter(EquipmentSchema.equipment_id == equipment_id).all()
