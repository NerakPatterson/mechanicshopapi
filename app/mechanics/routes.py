from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db
from models import Mechanic
from .schemas import mechanic_schema, mechanics_schema, mechanic_update_schema
from . import mechanic_bp   # import the blueprint

@mechanic_bp.route("/", methods=["POST"])
def create_mechanic():
    """POST /mechanics - Create a new mechanic."""
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Mechanic).where(Mechanic.email == mechanic_data.email)
    existing_mechanic = db.session.execute(query).scalars().first()
    if existing_mechanic:
        return jsonify({"error": "Email already associated with an existing mechanic"}), 409

    db.session.add(mechanic_data)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic_data), 201

@mechanic_bp.route("/", methods=["GET"])
def get_mechanics():
    """GET /mechanics - Get all mechanics."""
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics)

@mechanic_bp.route("/<int:mechanic_id>", methods=["GET"])
def get_mechanic(mechanic_id):
    """GET /mechanics/<int:mechanic_id> - Get a single mechanic."""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic not found."}), 404

@mechanic_bp.route("/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    """PUT /mechanics/<int:mechanic_id> - Update an existing mechanic."""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    try:
        mechanic_data_dict = mechanic_update_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_email = mechanic_data_dict.get("email")
    if new_email and new_email != mechanic.email:
        query = select(Mechanic).where(Mechanic.email == new_email)
        existing_mechanic = db.session.execute(query).scalars().first()
        if existing_mechanic and existing_mechanic.id != mechanic_id:
            return jsonify({"error": "Email already associated with another mechanic"}), 409

    for key, value in mechanic_data_dict.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanic_bp.route("/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):
    """DELETE /mechanics/<int:mechanic_id> - Delete a mechanic."""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} deleted successfully"}), 200
