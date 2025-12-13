# app/inventory/schemas.py
from extensions import ma
from models import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True
        exclude = ("tickets",)  # avoid nesting service tickets unless explicitly needed

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
