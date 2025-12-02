# app/mechanics/schemas.py
from extensions import ma
from models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        include_fk = True
        load_instance = True

# Full schema for create/read
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

# Update schema: allow partial updates
class MechanicUpdateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Mechanic
        load_instance = True

    name = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()
    address = ma.auto_field()
    salary = ma.auto_field()

mechanic_update_schema = MechanicUpdateSchema()
