from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db
from models import Mechanic
from schemas import mechanic_schema, mechanics_schema 

# --- API Endpoints defined at Module Level (Fixes Pylance visibility) ---

def create_mechanic():
    """POST /mechanics - Create a new mechanic."""
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check for email conflict
    query = select(Mechanic).where(Mechanic.email == mechanic_data.get('email'))
    existing_mechanic = db.session.execute(query).scalars().first()
    if existing_mechanic:
        return jsonify({"error": "Email already associated with an existing mechanic"}), 409

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

def get_mechanics():
    """GET /mechanics - Get all mechanics."""
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics)

def get_mechanic(mechanic_id):
    """GET /mechanics/<int:mechanic_id> - Get a single mechanic."""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic not found."}), 404

def update_mechanic(mechanic_id):
    """PUT /mechanics/<int:mechanic_id> - Update an existing mechanic."""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check for email conflict during update
    new_email = mechanic_data.get('email')
    if new_email and new_email != mechanic.email:
        query = select(Mechanic).where(Mechanic.email == new_email)
        existing_mechanic = db.session.execute(query).scalars().first()
        if existing_mechanic and existing_mechanic.id != mechanic_id:
            return jsonify({"error": "Email already associated with another mechanic"}), 409

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

def delete_mechanic(mechanic_id):
    """DELETE /mechanics/<int:mechanic_id> - Delete a mechanic."""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} deleted successfully"}), 200

# -------------------------------------------------------------------
# Route Registration
# -------------------------------------------------------------------

def register_mechanic_routes(app):
    """Binds mechanic CRUD routes to the Flask application."""
    app.add_url_rule("/mechanics", view_func=create_mechanic, methods=['POST'])
    app.add_url_rule("/mechanics", view_func=get_mechanics, methods=['GET'])
    app.add_url_rule("/mechanics/<int:mechanic_id>", view_func=get_mechanic, methods=['GET'])
    app.add_url_rule("/mechanics/<int:mechanic_id>", view_func=update_mechanic, methods=['PUT'])
    app.add_url_rule("/mechanics/<int:mechanic_id>", view_func=delete_mechanic, methods=['DELETE'])