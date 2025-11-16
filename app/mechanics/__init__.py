from flask import Blueprint

# Define the blueprint
mechanic_bp = Blueprint("mechanics", __name__)

# Import routes after blueprint is defined
from . import routes
