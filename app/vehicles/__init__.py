from flask import Blueprint

vehicle_bp = Blueprint("vehicles", __name__)

from . import routes  # import routes after blueprint is defined
