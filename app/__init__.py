from flask import Flask
from dotenv import load_dotenv
import os

from extensions import db, ma, migrate

def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.mechanics import mechanic_bp
    from app.customers import customer_bp
    from app.vehicles import vehicle_bp
    from app.service_tickets import ticket_bp
    from app.assignments import assignment_bp

    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(vehicle_bp, url_prefix="/vehicles")
    app.register_blueprint(ticket_bp, url_prefix="/tickets")
    app.register_blueprint(assignment_bp, url_prefix="/assignments")

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
