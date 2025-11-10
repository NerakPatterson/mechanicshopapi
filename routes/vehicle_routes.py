from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db
from models import Vehicle
from schemas import vehicle_schema, vehicles_schema 

# --- API Endpoints defined at Module Level (Fixes Pylance visibility) ---

def create_vehicle():
    """POST /vehicles - Create a new vehicle."""
    try:
        vehicle_data = vehicle_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check for VIN conflict
    if vehicle_data.get('vin'):
        query = select(Vehicle).where(Vehicle.vin == vehicle_data['vin'])
        existing_vehicle = db.session.execute(query).scalars().first()
        if existing_vehicle:
            return jsonify({"error": "VIN already registered."}), 409

    new_vehicle = Vehicle(**vehicle_data)
    db.session.add(new_vehicle)
    db.session.commit()
    return vehicle_schema.jsonify(new_vehicle), 201

def get_vehicles():
    """GET /vehicles - Get all vehicles."""
    query = select(Vehicle)
    vehicles = db.session.execute(query).scalars().all()
    return vehicles_schema.jsonify(vehicles)

def get_vehicle(vehicle_id):
    """GET /vehicles/<int:vehicle_id> - Get a single vehicle."""
    vehicle = db.session.get(Vehicle, vehicle_id)
    if vehicle:
        return vehicle_schema.jsonify(vehicle), 200
    return jsonify({"error": "Vehicle not found."}), 404

def update_vehicle(vehicle_id):
    """PUT /vehicles/<int:vehicle_id> - Update an existing vehicle."""
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404

    try:
        vehicle_data = vehicle_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check for VIN conflict during update
    new_vin = vehicle_data.get('vin')
    if new_vin and new_vin != vehicle.vin:
        query = select(Vehicle).where(Vehicle.vin == new_vin)
        existing_vehicle = db.session.execute(query).scalars().first()
        if existing_vehicle:
            return jsonify({"error": "VIN already associated with another vehicle"}), 409

    for key, value in vehicle_data.items():
        setattr(vehicle, key, value)

    db.session.commit()
    return vehicle_schema.jsonify(vehicle), 200

def delete_vehicle(vehicle_id):
    """DELETE /vehicles/<int:vehicle_id> - Delete a vehicle."""
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": f"Vehicle {vehicle_id} deleted successfully"}), 200

# -------------------------------------------------------------------
# Route Registration
# -------------------------------------------------------------------

def register_vehicle_routes(app):
    """Binds vehicle CRUD routes to the Flask application."""
    app.add_url_rule("/vehicles", view_func=create_vehicle, methods=['POST'])
    app.add_url_rule("/vehicles", view_func=get_vehicles, methods=['GET'])
    app.add_url_rule("/vehicles/<int:vehicle_id>", view_func=get_vehicle, methods=['GET'])
    app.add_url_rule("/vehicles/<int:vehicle_id>", view_func=update_vehicle, methods=['PUT'])
    app.add_url_rule("/vehicles/<int:vehicle_id>", view_func=delete_vehicle, methods=['DELETE'])