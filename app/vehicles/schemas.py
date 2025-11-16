from extensions import ma
from models import Vehicle

class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        load_instance = True
        include_fk = True   # include foreign keys if vehicle links to customer_id, etc.

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
