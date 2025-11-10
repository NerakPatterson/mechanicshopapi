from .customer_routes import register_customer_routes
from .vehicle_routes import register_vehicle_routes
from .ticket_routes import register_ticket_routes
from .mechanic_routes import register_mechanic_routes
from .assignment_routes import register_assignment_routes


def register_routes(app):
    register_customer_routes(app)
    register_vehicle_routes(app)
    register_ticket_routes(app)
    register_mechanic_routes(app)
    register_assignment_routes(app)