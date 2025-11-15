from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db
from models import ServiceAssignment, ServiceTicket, Mechanic
from schemas import assignment_schema, assignments_schema 

def create_assignment():
    """POST /assignments - Create a new service assignment."""
    try:
        # assignment_data is a ServiceAssignment model instance (due to load_instance=True)
        assignment_data = assignment_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Checking for existence of the ticket and mechanic IDs
    ticket_exists = db.session.get(ServiceTicket, assignment_data.service_ticket_id)
    mechanic_exists = db.session.get(Mechanic, assignment_data.mechanic_id)

    if not ticket_exists:
        return jsonify({"error": f"ServiceTicket ID {assignment_data.service_ticket_id} not found."}), 404
    if not mechanic_exists:
        return jsonify({"error": f"Mechanic ID {assignment_data.mechanic_id} not found."}), 404

    # Check for existing assignment (Prevent assigning the same ticket/mechanic twice)
    query = select(ServiceAssignment).where(
        ServiceAssignment.service_ticket_id == assignment_data.service_ticket_id,
        ServiceAssignment.mechanic_id == assignment_data.mechanic_id
    )
    existing_assignment = db.session.execute(query).scalars().first()
    
    if existing_assignment:
        return jsonify({"error": "This service ticket is already assigned to this mechanic."}), 409

    db.session.add(assignment_data)
    db.session.commit()
    # Standardized serialization
    return jsonify(assignment_schema.dump(assignment_data)), 201

def get_assignments():
    """GET /assignments - Get all service assignments."""
    query = select(ServiceAssignment)
    assignments = db.session.execute(query).scalars().all()
    # Standardized serialization
    return jsonify(assignments_schema.dump(assignments)), 200

def get_assignment(assignment_id):
    """GET /assignments/<int:assignment_id> - Get a single service assignment."""
    assignment = db.session.get(ServiceAssignment, assignment_id)
    if assignment:
        # Standardized serialization
        return jsonify(assignment_schema.dump(assignment)), 200
    return jsonify({"error": "Service assignment not found."}), 404

def update_assignment(assignment_id):
    """PUT /assignments/<int:assignment_id> - Update an existing service assignment."""
    assignment = db.session.get(ServiceAssignment, assignment_id)
    if not assignment:
        return jsonify({"error": "Service assignment not found."}), 404

    try:
        # Marshmallow updates the 'assignment' instance directly in place (updated_assignment is a model instance)
        updated_assignment = assignment_schema.load(
            request.json, 
            instance=assignment, 
            partial=True
        )
    except ValidationError as e:
        # Rollback any pending changes before returning error
        db.session.rollback()
        return jsonify(e.messages), 400

    # Validation logic for updated fields now uses the updated instance attributes (FIX)
    check_ticket_id = updated_assignment.service_ticket_id
    check_mechanic_id = updated_assignment.mechanic_id

    # 1. Check Foreign Keys (These checks only run if the IDs changed, or if schema.load was successful)
    if not db.session.get(ServiceTicket, check_ticket_id):
        db.session.rollback() 
        return jsonify({"error": f"ServiceTicket ID {check_ticket_id} not found."}), 404
    if not db.session.get(Mechanic, check_mechanic_id):
        db.session.rollback()
        return jsonify({"error": f"Mechanic ID {check_mechanic_id} not found."}), 404
        
    # 2. Check Unique Constraint (Prevent creating an identical assignment via update)
    query = select(ServiceAssignment).where(
        ServiceAssignment.service_ticket_id == check_ticket_id,
        ServiceAssignment.mechanic_id == check_mechanic_id
    )
    existing_assignment = db.session.execute(query).scalars().first()

    # If an existing assignment matches the *new* combination, ensure it's the current assignment being updated
    if existing_assignment and existing_assignment.id != assignment_id:
        db.session.rollback()
        return jsonify({"error": "This combination of ticket and mechanic is already assigned."}), 409

    db.session.commit()
    # Standardized serialization
    return jsonify(assignment_schema.dump(updated_assignment)), 200 

def delete_assignment(assignment_id):
    """DELETE /assignments/<int:assignment_id> - Delete a service assignment."""
    assignment = db.session.get(ServiceAssignment, assignment_id)
    if not assignment:
        return jsonify({"error": "Service assignment not found."}), 404

    db.session.delete(assignment)
    db.session.commit()
    return jsonify({"message": f"Service assignment {assignment_id} deleted successfully"}), 200

# Route Registration

def register_assignment_routes(app):
    """Binds service assignment CRUD routes to the Flask application."""
    app.add_url_rule("/assignments", view_func=create_assignment, methods=['POST'])
    app.add_url_rule("/assignments", view_func=get_assignments, methods=['GET'])
    app.add_url_rule("/assignments/<int:assignment_id>", view_func=get_assignment, methods=['GET'])
    app.add_url_rule("/assignments/<int:assignment_id>", view_func=update_assignment, methods=['PUT', 'PATCH'])
    app.add_url_rule("/assignments/<int:assignment_id>", view_func=delete_assignment, methods=['DELETE'])