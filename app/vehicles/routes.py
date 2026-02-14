from flask import request, jsonify, current_app
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from extensions import db, limiter, cache
from models import Vehicle
from .schemas import vehicle_schema, vehicles_schema
from . import vehicle_bp
from utils.decorators import auth_required


# GET /vehicles
@vehicle_bp.route("", methods=["GET"])
def get_vehicles():
    """
    GET /vehicles
    Returns all vehicles.
    Caching is DISABLED during tests to prevent request freezing.
    """
    if not current_app.config.get("TESTING"):
        # Only apply caching in production
        @cache.cached(timeout=120)
        def _cached():
            query = select(Vehicle)
            vehicles = db.session.execute(query).scalars().all()
            return jsonify(vehicles_schema.dump(vehicles)), 200
        return _cached()

    # Test mode: no caching wrapper
    query = select(Vehicle)
    vehicles = db.session.execute(query).scalars().all()
    return jsonify(vehicles_schema.dump(vehicles)), 200


# POST /vehicles
@vehicle_bp.route("", methods=["POST"])
@auth_required("admin", "mechanic")
def create_vehicle(user_id, role):
    """
    POST /vehicles
    Create a new vehicle.
    Rate limiting is disabled during tests.
    """
    if not current_app.config.get("TESTING"):
        limiter.limit("10 per hour")(create_vehicle)

    try:
        vehicle_data = vehicle_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # VIN uniqueness check
    if vehicle_data.vin:
        existing = db.session.execute(
            select(Vehicle).where(Vehicle.vin == vehicle_data.vin)
        ).scalars().first()

        if existing:
            return jsonify({"error": "VIN already registered."}), 409

    db.session.add(vehicle_data)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during vehicle creation."}), 500

    return jsonify({
        "message": f"Vehicle created by {role} (user {user_id})",
        "vehicle": vehicle_schema.dump(vehicle_data)
    }), 201


# GET /vehicles/<id>
@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404
    return jsonify(vehicle_schema.dump(vehicle)), 200


# PUT /vehicles/<id>
@vehicle_bp.route("/<int:vehicle_id>", methods=["PUT"])
@auth_required("admin", "mechanic")
def update_vehicle(user_id, role, vehicle_id):
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404

    original_vin = vehicle.vin

    try:
        updated_vehicle = vehicle_schema.load(
            request.json,
            instance=vehicle,
            partial=True
        )
    except ValidationError as e:
        return jsonify(e.messages), 400

    # VIN uniqueness check
    new_vin = updated_vehicle.vin
    if new_vin and new_vin != original_vin:
        existing = db.session.execute(
            select(Vehicle).where(Vehicle.vin == new_vin)
        ).scalars().first()

        if existing and existing.id != updated_vehicle.id:
            db.session.rollback()
            return jsonify({"error": "VIN already associated with another vehicle"}), 409

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error during update."}), 500

    return jsonify({
        "message": f"Vehicle updated by {role} (user {user_id})",
        "vehicle": vehicle_schema.dump(updated_vehicle)
    }), 200


# DELETE /vehicles/<id>
@vehicle_bp.route("/<int:vehicle_id>", methods=["DELETE"])
@auth_required("admin")
def delete_vehicle(user_id, role, vehicle_id):
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404

    db.session.delete(vehicle)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during deletion."}), 500

    return jsonify({"message": f"Vehicle {vehicle_id} deleted by admin (user {user_id})"}), 200