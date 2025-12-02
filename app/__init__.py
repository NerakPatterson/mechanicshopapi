from flask import Flask
from dotenv import load_dotenv
import os
from extensions import db, ma, migrate, limiter, cache
from app.inventory import inventory_bp


def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Optional cache config
    app.config['CACHE_TYPE'] = 'SimpleCache'  # or 'RedisCache', etc.

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
    from app.inventory import inventory_bp   # <-- new import

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(vehicle_bp, url_prefix="/vehicles")
    app.register_blueprint(ticket_bp, url_prefix="/tickets")
    app.register_blueprint(assignment_bp, url_prefix="/assignments")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
