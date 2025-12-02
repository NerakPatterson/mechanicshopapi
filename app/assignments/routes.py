from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db, limiter, cache
from models import ServiceAssignment, ServiceTicket, Mechanic
from .schemas import assignment_schema, assignments_schema
from . import assignment_bp
from utils.decorators import auth_required   # unified decorator

@assignment_bp.route("/", methods=["GET"])
@cache.cached(timeout=45)
def list_assignments():
    """GET /assignments - Cached list of assignments (ticket + mechanic IDs)."""
    assignments = ServiceAssignment.query.all()
    return jsonify({
        "assignments": [{"ticket": a.service_ticket_id, "mechanic": a.mechanic_id} for a in assignments]
    }), 200

@assignment_bp.route("/", methods=["POST"])
@auth_required("admin", "mechanic")   # restrict creation
@limiter.limit("15 per day")
def create_assignment(user_id, role):
    """POST /assignments - Create a new service assignment (admin/mechanic only)."""
    try:
        assignment_data = assignment_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    ticket_exists = db.session.get(ServiceTicket, assignment_data.service_ticket_id)
    mechanic_exists = db.session.get(Mechanic, assignment_data.mechanic_id)

    if not ticket_exists:
        return jsonify({"error": f"ServiceTicket ID {assignment_data.service_ticket_id} not found."}), 404
    if not mechanic_exists:
        return jsonify({"error": f"Mechanic ID {assignment_data.mechanic_id} not found."}), 404

    query = select(ServiceAssignment).where(
        ServiceAssignment.service_ticket_id == assignment_data.service_ticket_id,
        ServiceAssignment.mechanic_id == assignment_data.mechanic_id
    )
    existing_assignment = db.session.execute(query).scalars().first()
    if existing_assignment:
        return jsonify({"error": "This service ticket is already assigned to this mechanic."}), 409

    db.session.add(assignment_data)
    db.session.commit()
    return jsonify({
        "message": f"Assignment created by {role} (user {user_id})",
        "assignment": assignment_schema.dump(assignment_data)
    }), 201

@assignment_bp.route("/", methods=["GET"])
def get_assignments():
    """GET /assignments - Get all service assignments."""
    query = select(ServiceAssignment)
    assignments = db.session.execute(query).scalars().all()
    return jsonify(assignments_schema.dump(assignments)), 200

@assignment_bp.route("/<int:assignment_id>", methods=["GET"])
def get_assignment(assignment_id):
    """GET /assignments/<assignment_id> - Get a single service assignment."""
    assignment = db.session.get(ServiceAssignment, assignment_id)
    if assignment:
        return jsonify(assignment_schema.dump(assignment)), 200
    return jsonify({"error": "Service assignment not found."}), 404

@assignment_bp.route("/<int:assignment_id>", methods=["PUT", "PATCH"])
@auth_required("admin", "mechanic")   # restrict updates
def update_assignment(user_id, role, assignment_id):
    """PUT/PATCH /assignments/<assignment_id> - Update an existing service assignment."""
    assignment = db.session.get(ServiceAssignment, assignment_id)
    if not assignment:
        return jsonify({"error": "Service assignment not found."}), 404

    try:
        updated_assignment = assignment_schema.load(
            request.json,
            instance=assignment,
            partial=True
        )
    except ValidationError as e:
        db.session.rollback()
        return jsonify(e.messages), 400

    check_ticket_id = updated_assignment.service_ticket_id
    check_mechanic_id = updated_assignment.mechanic_id

    if not db.session.get(ServiceTicket, check_ticket_id):
        db.session.rollback()
        return jsonify({"error": f"ServiceTicket ID {check_ticket_id} not found."}), 404
    if not db.session.get(Mechanic, check_mechanic_id):
        db.session.rollback()
        return jsonify({"error": f"Mechanic ID {check_mechanic_id} not found."}), 404

    query = select(ServiceAssignment).where(
        ServiceAssignment.service_ticket_id == check_ticket_id,
        ServiceAssignment.mechanic_id == check_mechanic_id
    )
    existing_assignment = db.session.execute(query).scalars().first()
    if existing_assignment and existing_assignment.id != assignment_id:
        db.session.rollback()
        return jsonify({"error": "This combination of ticket and mechanic is already assigned."}), 409

    db.session.commit()
    return jsonify({
        "message": f"Assignment updated by {role} (user {user_id})",
        "assignment": assignment_schema.dump(updated_assignment)
    }), 200

@assignment_bp.route("/<int:assignment_id>", methods=["DELETE"])
@auth_required("admin")   # only admins can delete
def delete_assignment(user_id, role, assignment_id):
    """DELETE /assignments/<assignment_id> - Delete a service assignment (admin only)."""
    assignment = db.session.get(ServiceAssignment, assignment_id)
    if not assignment:
        return jsonify({"error": "Service assignment not found."}), 404

    db.session.delete(assignment)
    db.session.commit()
    return jsonify({"message": f"Service assignment {assignment_id} deleted by admin (user {user_id})"}), 200
