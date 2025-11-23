from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db
from models import Vehicle
from .schemas import vehicle_schema, vehicles_schema
from . import vehicle_bp
from flask import Blueprint, request
from extensions import limiter, cache, db
from models import Vehicle

vehicle_bp = Blueprint("vehicles", __name__)

@vehicle_bp.route("/", methods=["GET"])
@cache.cached(timeout=120)
def list_vehicles():
    vehicles = Vehicle.query.all()
    return {"vehicles": [v.vin for v in vehicles]}

@vehicle_bp.route("/", methods=["POST"])
@limiter.limit("10 per hour")
def create_vehicle():
    data = request.json
    new_vehicle = Vehicle(**data)
    db.session.add(new_vehicle)
    db.session.commit()
    return {"message": "Vehicle created"}, 201


@vehicle_bp.route("/", methods=["POST"])
def create_vehicle():
    """POST /vehicles - Create a new vehicle."""
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
    return jsonify(vehicle_schema.dump(vehicle_data)), 201

@vehicle_bp.route("/", methods=["GET"])
def get_vehicles():
    """GET /vehicles - Get all vehicles."""
    query = select(Vehicle)
    vehicles = db.session.execute(query).scalars().all()
    return jsonify(vehicles_schema.dump(vehicles)), 200

@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    """GET /vehicles/<int:vehicle_id> - Get a single vehicle."""
    vehicle = db.session.get(Vehicle, vehicle_id)
    if vehicle:
        return jsonify(vehicle_schema.dump(vehicle)), 200
    return jsonify({"error": "Vehicle not found."}), 404

@vehicle_bp.route("/<int:vehicle_id>", methods=["PUT"])
def update_vehicle(vehicle_id):
    """PUT /vehicles/<int:vehicle_id> - Update an existing vehicle."""
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
    return jsonify(vehicle_schema.dump(updated_vehicle)), 200

@vehicle_bp.route("/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    """DELETE /vehicles/<int:vehicle_id> - Delete a vehicle."""
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": f"Vehicle {vehicle_id} deleted successfully"}), 200
