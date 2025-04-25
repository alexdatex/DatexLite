from sqlalchemy.orm import Session

from ..models.equipment_schema import EquipmentSchema


class EquipmentSchemaService:
    @staticmethod
    def get_schemas(db: Session, equipment_id: int):
        return db.query(EquipmentSchema).filter(EquipmentSchema.equipment_id == equipment_id,
                                                EquipmentSchema.is_deleted == False).all()

    @staticmethod
    def get_schema(db: Session, schema_id: int):
        return db.query(EquipmentSchema).filter(EquipmentSchema.id == schema_id).first()
