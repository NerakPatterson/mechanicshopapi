from extensions import ma
from models import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        include_fk = True
        load_instance = True

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
