from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db
from models import ServiceTicket
from schemas import ticket_schema, tickets_schema 

# --- API Endpoints defined at Module Level (Fixes Pylance visibility) ---

def create_ticket():
    """POST /tickets - Create a new service ticket."""
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

def get_tickets():
    """GET /tickets - Get all service tickets."""
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(tickets)

def get_ticket(ticket_id):
    """GET /tickets/<int:ticket_id> - Get a single service ticket."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if ticket:
        return ticket_schema.jsonify(ticket), 200
    return jsonify({"error": "Service ticket not found."}), 404

def update_ticket(ticket_id):
    """PUT /tickets/<int:ticket_id> - Update an existing service ticket."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    try:
        ticket_data = ticket_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in ticket_data.items():
        setattr(ticket, key, value)

    db.session.commit()
    return ticket_schema.jsonify(ticket), 200

def delete_ticket(ticket_id):
    """DELETE /tickets/<int:ticket_id> - Delete a service ticket."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Service ticket {ticket_id} deleted successfully"}), 200

# -------------------------------------------------------------------
# Route Registration
# -------------------------------------------------------------------

def register_ticket_routes(app):
    """Binds service ticket CRUD routes to the Flask application."""
    app.add_url_rule("/tickets", view_func=create_ticket, methods=['POST'])
    app.add_url_rule("/tickets", view_func=get_tickets, methods=['GET'])
    app.add_url_rule("/tickets/<int:ticket_id>", view_func=get_ticket, methods=['GET'])
    app.add_url_rule("/tickets/<int:ticket_id>", view_func=update_ticket, methods=['PUT'])
    app.add_url_rule("/tickets/<int:ticket_id>", view_func=delete_ticket, methods=['DELETE'])