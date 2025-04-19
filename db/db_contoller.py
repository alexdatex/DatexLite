import db
from db.models import EquipmentSchema
from db.models.mark import Mark
from db.models.mark_image import MarkImage
from db.services import ComponentService, EquipmentSchemaService, MarkService, MarkImageService


class DBController:
    def __init__(self, db):
        self.db = db

    def get_component(self, component_id: int):
        return ComponentService.get_component(self.db, component_id)

    def add_schema(self, schema: EquipmentSchema):
        self.db.add(schema)
        return self.db.commit()

    def get_schemas(self, equipment_id: int):
        return EquipmentSchemaService.get_schemas(self.db, equipment_id)

    def get_schema(self, schema_id: int):
        return EquipmentSchemaService.get_schema(self.db, schema_id)

    def add_mark(self, mark: Mark):
        self.db.add(mark)
        self.db.commit()

    def get_mark(self, mark_id: int):
        return MarkService.get_mark(self.db, mark_id)

    def get_marks(self, schema_id: int):
        return MarkService.get_marks(self.db, schema_id)

    def add_mark_image(self, mark_image: MarkImage):
        self.db.add(mark_image)
        self.db.commit()

    def get_mark_image(self, mark_image_id: int):
        return MarkImageService.get_mark_image(self.db, mark_image_id)

    def get_mark_images(self, mark_id: int):
        return MarkImageService.get_mark_images(self.db, mark_id)
