from flask import Flask
from dotenv import load_dotenv
import os
from extensions import db, ma, migrate, limiter, cache
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API's Name"
    }
)

def create_app(config_class=None):
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # If a config class is provided (ProductionConfig), use it
    if config_class:
        app.config.from_object(config_class)
    else:
        # Default to environment variables for local development
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    # Optional cache config
    app.config['CACHE_TYPE'] = 'SimpleCache'

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)

    # Import and register blueprints
    from app.users import user_bp
    from app.mechanics import mechanic_bp
    from app.customers import customer_bp
    from app.vehicles import vehicle_bp
    from app.service_tickets import ticket_bp
    from app.assignments import assignment_bp
    from app.inventory import inventory_bp

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(vehicle_bp, url_prefix="/vehicles")
    app.register_blueprint(ticket_bp, url_prefix="/tickets")
    app.register_blueprint(assignment_bp, url_prefix="/assignments")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Import models inside app context so SQLAlchemy sees them
    with app.app_context():
        from models import User, Mechanic, Customer, Vehicle, ServiceTicket, ServiceAssignment, Inventory
        db.create_all()

    return app