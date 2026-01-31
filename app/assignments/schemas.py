from extensions import ma
from models import ServiceAssignment
from app.mechanics.schemas import MechanicSchema
from app.service_tickets.schemas import ServiceTicketSchema

class ServiceAssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceAssignment
        load_instance = True
        include_fk = True

    mechanic = ma.Nested(MechanicSchema)
    ticket = ma.Nested(ServiceTicketSchema)

assignment_schema = ServiceAssignmentSchema()
assignments_schema = ServiceAssignmentSchema(many=True)