# app/service_tickets/schemas.py
from extensions import ma
from models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True   # include vehicle_id foreign key

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
