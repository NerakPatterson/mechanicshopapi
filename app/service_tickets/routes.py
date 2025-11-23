from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db
from models import ServiceTicket
from .schemas import ticket_schema, tickets_schema
from . import ticket_bp
from flask import Blueprint, request
from extensions import limiter, cache, db
from models import ServiceTicket

ticket_bp = Blueprint("tickets", __name__)

@ticket_bp.route("/", methods=["GET"])
@cache.cached(timeout=30)
def list_tickets():
    tickets = ServiceTicket.query.all()
    return {"tickets": [t.status for t in tickets]}

@ticket_bp.route("/", methods=["POST"])
@limiter.limit("20 per day")
def create_ticket():
    data = request.json
    new_ticket = ServiceTicket(**data)
    db.session.add(new_ticket)
    db.session.commit()
    return {"message": "Ticket created"}, 201


@ticket_bp.route("/", methods=["POST"])
def create_ticket():
    """POST /tickets - Create a new service ticket."""
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(ticket_data)
    db.session.commit()
    return ticket_schema.jsonify(ticket_data), 201

@ticket_bp.route("/", methods=["GET"])
def get_tickets():
    """GET /tickets - Get all service tickets."""
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(tickets)

@ticket_bp.route("/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    """GET /tickets/<int:ticket_id> - Get a single service ticket."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if ticket:
        return ticket_schema.jsonify(ticket), 200
    return jsonify({"error": "Service ticket not found."}), 404

@ticket_bp.route("/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):
    """PUT /tickets/<int:ticket_id> - Update an existing service ticket."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    try:
        ticket = ticket_schema.load(request.json, instance=ticket, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return ticket_schema.jsonify(ticket), 200

@ticket_bp.route("/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    """DELETE /tickets/<int:ticket_id> - Delete a service ticket."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Service ticket {ticket_id} deleted successfully"}), 200
