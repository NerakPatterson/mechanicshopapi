from extensions import ma
from models import Customer, Vehicle, ServiceTicket, Mechanic, ServiceAssignment

# Customer Schema
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Vehicle Schema
class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        load_instance = True
        include_fk = True

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)

# ServiceTicket Schema
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)

# Mechanic Schema
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

# ServiceAssignment Schema
class ServiceAssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceAssignment
        load_instance = True
        include_fk = True

assignment_schema = ServiceAssignmentSchema()
assignments_schema = ServiceAssignmentSchema(many=True)