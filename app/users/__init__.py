from flask import Blueprint

# Define the blueprint for users
user_bp = Blueprint("users", __name__, url_prefix="/users")

# Import routes after blueprint is defined
from . import routes  # imported for side effects
