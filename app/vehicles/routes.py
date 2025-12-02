from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db, limiter, cache
from models import Vehicle
from .schemas import vehicle_schema, vehicles_schema
from . import vehicle_bp
from utils.decorators import auth_required   # unified decorator

@vehicle_bp.route("/", methods=["GET"])
@cache.cached(timeout=120)
def get_vehicles():
    """GET /vehicles - Cached list of all vehicles."""
    query = select(Vehicle)
    vehicles = db.session.execute(query).scalars().all()
    return jsonify(vehicles_schema.dump(vehicles)), 200

@vehicle_bp.route("/", methods=["POST"])
@auth_required("admin", "mechanic")   # restrict creation
@limiter.limit("10 per hour")
def create_vehicle(user_id, role):
    """POST /vehicles - Create a new vehicle (admin/mechanic only)."""
    try:
        vehicle_data = vehicle_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if vehicle_data.vin:
        query = select(Vehicle).where(Vehicle.vin == vehicle_data.vin)
        existing_vehicle = db.session.execute(query).scalars().first()
        if existing_vehicle:
            return jsonify({"error": "VIN already registered."}), 409

    db.session.add(vehicle_data)
    db.session.commit()
    return jsonify({
        "message": f"Vehicle created by {role} (user {user_id})",
        "vehicle": vehicle_schema.dump(vehicle_data)
    }), 201

@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    """GET /vehicles/<vehicle_id> - Get a single vehicle."""
    vehicle = db.session.get(Vehicle, vehicle_id)
    if vehicle:
        return jsonify(vehicle_schema.dump(vehicle)), 200
    return jsonify({"error": "Vehicle not found."}), 404

@vehicle_bp.route("/<int:vehicle_id>", methods=["PUT"])
@auth_required("admin", "mechanic")   # restrict updates
def update_vehicle(user_id, role, vehicle_id):
    """PUT /vehicles/<vehicle_id> - Update an existing vehicle (admin/mechanic only)."""
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

    new_vin = updated_vehicle.vin
    if new_vin and new_vin != original_vin:
        query = select(Vehicle).where(Vehicle.vin == new_vin)
        existing_vehicle = db.session.execute(query).scalars().first()
        if existing_vehicle and existing_vehicle.id != updated_vehicle.id:
            db.session.rollback()
            return jsonify({"error": "VIN already associated with another vehicle"}), 409

    db.session.commit()
    return jsonify({
        "message": f"Vehicle updated by {role} (user {user_id})",
        "vehicle": vehicle_schema.dump(updated_vehicle)
    }), 200

@vehicle_bp.route("/<int:vehicle_id>", methods=["DELETE"])
@auth_required("admin")   # only admins can delete
def delete_vehicle(user_id, role, vehicle_id):
    """DELETE /vehicles/<vehicle_id> - Delete a vehicle (admin only)."""
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": f"Vehicle {vehicle_id} deleted by admin (user {user_id})"}), 200
