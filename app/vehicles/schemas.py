# app/vehicles/schemas.py
from extensions import ma
from models import Vehicle

class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        load_instance = True
        include_fk = True   # include customer_id foreign key

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
