# app/mechanics/schemas.py
from extensions import ma
from models import Mechanic
from marshmallow import fields

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True
        exclude = ("assignments",)  # avoid nesting service assignments unless needed

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


# Proper partial update schema
class MechanicUpdateSchema(ma.Schema):
    name = fields.String()
    email = fields.Email()
    phone = fields.String()
    address = fields.String()
    salary = fields.Decimal(as_string=True)

mechanic_update_schema = MechanicUpdateSchema()
