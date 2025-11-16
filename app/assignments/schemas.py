from extensions import ma
from models import ServiceAssignment

class ServiceAssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceAssignment
        load_instance = True
        include_fk = True   # include foreign keys for ticket_id and mechanic_id

assignment_schema = ServiceAssignmentSchema()
assignments_schema = ServiceAssignmentSchema(many=True)
