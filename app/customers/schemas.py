# app/customers/schemas.py
from extensions import ma
from models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_fk = True
        load_instance = True

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
