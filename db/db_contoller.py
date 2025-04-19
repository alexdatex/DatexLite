from db.services import ComponentService

class DBController:
    def __init__(self, db):
        self.db = db

    def get_component(self, component_id: int):
        return ComponentService.get_component(self.db, component_id)
