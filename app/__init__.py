from flask import Flask
from dotenv import load_dotenv
import os

from extensions import db, ma, migrate, limiter, cache, jwt
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Your API's Name"}
)


def create_app(config_class=None):
    load_dotenv()

    app = Flask(__name__)

    # Load config
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
        app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

    # Initialize extensions AFTER config is set
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)
    jwt.init_app(app)

    # Register blueprints
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

    # DO NOT create tables here — tests will handle it
    return app
