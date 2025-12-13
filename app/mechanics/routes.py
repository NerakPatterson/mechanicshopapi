from flask import request, jsonify
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from extensions import db, limiter, cache
from models import Mechanic, ServiceAssignment
from .schemas import mechanic_schema, mechanics_schema, mechanic_update_schema
from . import mechanic_bp
from utils.decorators import auth_required   # unified decorator


# GET ranked mechanics
@mechanic_bp.route("/ranked", methods=["GET"])
def ranked_mechanics():
    """GET /mechanics/ranked - List mechanics ordered by ticket count."""
    query = (
        db.session.query(Mechanic, func.count(ServiceAssignment.id).label("ticket_count"))
        .join(ServiceAssignment, Mechanic.id == ServiceAssignment.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(func.count(ServiceAssignment.id).desc())
    )
    results = query.all()

    return jsonify([
        {"id": mech.id, "name": mech.name, "ticket_count": count}
        for mech, count in results
    ]), 200


# GET all mechanics
@mechanic_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_mechanics():
    """GET /mechanics - Get all mechanics."""
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return jsonify(mechanics_schema.dump(mechanics)), 200


# CREATE mechanic (admin only)
@mechanic_bp.route("/", methods=["POST"])
@auth_required("admin")
@limiter.limit("5 per hour")
def create_mechanic(user_id, role):
    """POST /mechanics - Create a new mechanic (admin only)."""
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Mechanic).where(Mechanic.email == mechanic_data.email)
    existing_mechanic = db.session.execute(query).scalars().first()
    if existing_mechanic:
        return jsonify({"error": "Email already associated with an existing mechanic"}), 409

    db.session.add(mechanic_data)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during mechanic creation"}), 500

    return jsonify({
        "message": f"Mechanic created by admin (user {user_id})",
        "mechanic": mechanic_schema.dump(mechanic_data)
    }), 201


# GET single mechanic
@mechanic_bp.route("/<int:mechanic_id>", methods=["GET"])
def get_mechanic(mechanic_id):
    """GET /mechanics/<mechanic_id> - Get a single mechanic."""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic:
        return jsonify(mechanic_schema.dump(mechanic)), 200
    return jsonify({"error": "Mechanic not found."}), 404


# UPDATE mechanic (admin only)
@mechanic_bp.route("/<int:mechanic_id>", methods=["PUT"])
@auth_required("admin")
def update_mechanic(user_id, role, mechanic_id):
    """PUT /mechanics/<mechanic_id> - Update an existing mechanic (admin only)."""
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

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during update"}), 500

    return jsonify({
        "message": f"Mechanic updated by admin (user {user_id})",
        "mechanic": mechanic_schema.dump(mechanic)
    }), 200


# DELETE mechanic (admin only)
@mechanic_bp.route("/<int:mechanic_id>", methods=["DELETE"])
@auth_required("admin")
def delete_mechanic(user_id, role, mechanic_id):
    """DELETE /mechanics/<mechanic_id> - Delete a mechanic (admin only)."""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    db.session.delete(mechanic)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during deletion"}), 500

    return jsonify({"message": f"Mechanic {mechanic_id} deleted by admin (user {user_id})"}), 200
