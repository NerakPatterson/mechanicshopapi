from extensions import ma
from models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True   # include foreign keys if your ticket has customer_id, vehicle_id, etc.

# Single ticket schema
ticket_schema = ServiceTicketSchema()

# Multiple tickets schema
tickets_schema = ServiceTicketSchema(many=True)
