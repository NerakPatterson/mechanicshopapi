from flask import Blueprint

ticket_bp = Blueprint("tickets", __name__)

from . import routes  # import routes after blueprint is defined
