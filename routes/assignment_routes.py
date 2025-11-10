from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db
from models import ServiceAssignment
from schemas import assignment_schema, assignments_schema 

# --- API Endpoints defined at Module Level (Fixes Pylance visibility) ---

def create_assignment():
    """POST /assignments - Create a new service assignment."""
    try:
        assignment_data = assignment_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_assignment = ServiceAssignment(**assignment_data)
    db.session.add(new_assignment)
    db.session.commit()
    return assignment_schema.jsonify(new_assignment), 201

def get_assignments():
    """GET /assignments - Get all service assignments."""
    query = select(ServiceAssignment)
    assignments = db.session.execute(query).scalars().all()
    return assignments_schema.jsonify(assignments)

def get_assignment(assignment_id):
    """GET /assignments/<int:assignment_id> - Get a single service assignment."""
    assignment = db.session.get(ServiceAssignment, assignment_id)
    if assignment:
        return assignment_schema.jsonify(assignment), 200
    return jsonify({"error": "Service assignment not found."}), 404

def update_assignment(assignment_id):
    """PUT /assignments/<int:assignment_id> - Update an existing service assignment."""
    assignment = db.session.get(ServiceAssignment, assignment_id)
    if not assignment:
        return jsonify({"error": "Service assignment not found."}), 404

    try:
        assignment_data = assignment_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in assignment_data.items():
        setattr(assignment, key, value)

    db.session.commit()
    return assignment_schema.jsonify(assignment), 200

def delete_assignment(assignment_id):
    """DELETE /assignments/<int:assignment_id> - Delete a service assignment."""
    assignment = db.session.get(ServiceAssignment, assignment_id)
    if not assignment:
        return jsonify({"error": "Service assignment not found."}), 404

    db.session.delete(assignment)
    db.session.commit()
    return jsonify({"message": f"Service assignment {assignment_id} deleted successfully"}), 200

# -------------------------------------------------------------------
# Route Registration
# -------------------------------------------------------------------

def register_assignment_routes(app):
    """Binds service assignment CRUD routes to the Flask application."""
    app.add_url_rule("/assignments", view_func=create_assignment, methods=['POST'])
    app.add_url_rule("/assignments", view_func=get_assignments, methods=['GET'])
    app.add_url_rule("/assignments/<int:assignment_id>", view_func=get_assignment, methods=['GET'])
    app.add_url_rule("/assignments/<int:assignment_id>", view_func=update_assignment, methods=['PUT'])
    app.add_url_rule("/assignments/<int:assignment_id>", view_func=delete_assignment, methods=['DELETE'])