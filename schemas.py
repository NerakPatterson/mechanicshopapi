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

# Mechanic Schema for Creation/Retrieval (returns model instance)
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

# Mechanic Schema for Updates (returns a standard dictionary)
# This is used for PUT/PATCH methods where we only want the dictionary data,
# not a model instance, so we can check individual fields like 'email'.
class MechanicUpdateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        # Explicitly set load_instance to False (default) to ensure load() returns a dictionary.
        load_instance = False 

mechanic_update_schema = MechanicUpdateSchema() # NEW instance for updates

# ServiceAssignment Schema
class ServiceAssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceAssignment
        load_instance = True
        include_fk = True

assignment_schema = ServiceAssignmentSchema()
assignments_schema = ServiceAssignmentSchema(many=True)