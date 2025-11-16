from flask import Blueprint

assignment_bp = Blueprint("assignments", __name__)

from . import routes  # import routes after blueprint is defined
