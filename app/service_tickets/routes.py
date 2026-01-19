from flask import request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from extensions import db, limiter, cache
from models import ServiceTicket, Mechanic, ServiceAssignment, Inventory
from .schemas import ticket_schema, tickets_schema
from . import ticket_bp
from utils.decorators import auth_required   # unified decorator

# Add a part to a service ticket
@ticket_bp.route("/<int:ticket_id>/add_part", methods=["POST"])
@auth_required("admin", "mechanic")
def add_part_to_ticket(user_id, role, ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service Ticket not found"}), 404

    data = request.json
    part_id = data.get("part_id")
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Inventory part not found"}), 404

    ticket.parts.append(part)  # matches model relationship
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error adding part"}), 500

    return jsonify({"message": f"Part {part_id} added to ticket {ticket_id}"}), 200


@ticket_bp.route("", methods=["GET"])
@cache.cached(timeout=30)
def get_tickets():
    """GET /tickets - Cached list of all service tickets."""
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return jsonify(tickets_schema.dump(tickets)), 200


@ticket_bp.route("", methods=["POST"])
@auth_required("admin", "mechanic")   # restrict creation
@limiter.limit("20 per day")
def create_ticket(user_id, role):
    """POST /tickets - Create a new service ticket (admin/mechanic only)."""
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(ticket_data)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during ticket creation"}), 500

    return jsonify({
        "message": f"Ticket created by {role} (user {user_id})",
        "ticket": ticket_schema.dump(ticket_data)
    }), 201


@ticket_bp.route("/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    """GET /tickets/<ticket_id> - Get a single service ticket."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if ticket:
        return jsonify(ticket_schema.dump(ticket)), 200
    return jsonify({"error": "Service ticket not found."}), 404


@ticket_bp.route("/<int:ticket_id>", methods=["PUT"])
@auth_required("admin", "mechanic")   # restrict updates
def update_ticket(user_id, role, ticket_id):
    """PUT /tickets/<ticket_id> - Update an existing service ticket (admin/mechanic only)."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    try:
        updated_ticket = ticket_schema.load(request.json, instance=ticket, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during update"}), 500

    return jsonify({
        "message": f"Ticket updated by {role} (user {user_id})",
        "ticket": ticket_schema.dump(updated_ticket)
    }), 200


@ticket_bp.route("/<int:ticket_id>", methods=["DELETE"])
@auth_required("admin")   # only admins can delete
def delete_ticket(user_id, role, ticket_id):
    """DELETE /tickets/<ticket_id> - Delete a service ticket (admin only)."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    db.session.delete(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during deletion"}), 500

    return jsonify({"message": f"Service ticket {ticket_id} deleted by admin (user {user_id})"}), 200


@ticket_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
@auth_required("admin", "mechanic")   # restrict mechanic editing
def edit_ticket(user_id, role, ticket_id):
    """PUT /tickets/<ticket_id>/edit - Add/remove mechanics via query params (admin/mechanic only)."""
    data = request.args
    add_ids = data.getlist("add_ids")
    remove_ids = data.getlist("remove_ids")

    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    # Add mechanics via ServiceAssignment
    for mid in add_ids:
        mechanic = db.session.get(Mechanic, int(mid))
        if mechanic:
            existing = db.session.query(ServiceAssignment).filter_by(
                service_ticket_id=ticket.id, mechanic_id=mechanic.id
            ).first()
            if not existing:
                assignment = ServiceAssignment(service_ticket_id=ticket.id, mechanic_id=mechanic.id)
                db.session.add(assignment)

    # Remove mechanics via ServiceAssignment
    for mid in remove_ids:
        mechanic = db.session.get(Mechanic, int(mid))
        if mechanic:
            assignment = db.session.query(ServiceAssignment).filter_by(
                service_ticket_id=ticket.id, mechanic_id=mechanic.id
            ).first()
            if assignment:
                db.session.delete(assignment)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error updating mechanics"}), 500

    return jsonify({
        "message": f"Ticket {ticket_id} mechanics updated by {role} (user {user_id})"
    }), 200
