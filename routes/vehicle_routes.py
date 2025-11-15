from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db
from models import Vehicle
from schemas import vehicle_schema, vehicles_schema 

def create_vehicle():
    """POST /vehicles - Create a new vehicle."""
    try:
        # vehicle_data is a Vehicle model instance because load_instance=True is assumed on the schema
        vehicle_data = vehicle_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Access VIN using dot notation (.vin)
    if vehicle_data.vin:
        query = select(Vehicle).where(Vehicle.vin == vehicle_data.vin)
        existing_vehicle = db.session.execute(query).scalars().first()
        if existing_vehicle:
            return jsonify({"error": "VIN already registered."}), 409

    # Since Marshmallow already returned the instance, we add it directly
    db.session.add(vehicle_data)
    db.session.commit()
    return jsonify(vehicle_schema.dump(vehicle_data)), 201

def get_vehicles():
    """GET /vehicles - Get all vehicles."""
    query = select(Vehicle)
    vehicles = db.session.execute(query).scalars().all()
    return jsonify(vehicles_schema.dump(vehicles)), 200

def get_vehicle(vehicle_id):
    """GET /vehicles/<int:vehicle_id> - Get a single vehicle."""
    vehicle = db.session.get(Vehicle, vehicle_id)
    if vehicle:
        return jsonify(vehicle_schema.dump(vehicle)), 200
    return jsonify({"error": "Vehicle not found."}), 404

def update_vehicle(vehicle_id):
    """PUT /vehicles/<int:vehicle_id> - Update an existing vehicle."""
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404

    # Store the original VIN to check for conflicts after the instance is updated
    original_vin = vehicle.vin

    try:
        # Load and update the existing model instance in place using the 'instance' argument.
        updated_vehicle = vehicle_schema.load(
            request.json,
            instance=vehicle, 
            partial=True
        )
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check for VIN conflict after the update has been applied to the instance
    new_vin = updated_vehicle.vin
    
    if new_vin and new_vin != original_vin:
        query = select(Vehicle).where(Vehicle.vin == new_vin)
        existing_vehicle = db.session.execute(query).scalars().first()

        # Correct conflict check: ensure the conflicting VIN belongs to a *different* vehicle.
        if existing_vehicle and existing_vehicle.id != updated_vehicle.id:
            # Rollback the session to discard the VIN change applied by schema.load before erroring out.
            db.session.rollback()
            return jsonify({"error": "VIN already associated with another vehicle"}), 409

    # Since Marshmallow updated the instance directly, we just commit.
    db.session.commit()
    return jsonify(vehicle_schema.dump(updated_vehicle)), 200

def delete_vehicle(vehicle_id):
    """DELETE /vehicles/<int:vehicle_id> - Delete a vehicle."""
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found."}), 404

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": f"Vehicle {vehicle_id} deleted successfully"}), 200


# Route Registration

def register_vehicle_routes(app):
    """Binds vehicle CRUD routes to the Flask application."""
    app.add_url_rule("/vehicles", view_func=create_vehicle, methods=['POST'])
    app.add_url_rule("/vehicles", view_func=get_vehicles, methods=['GET'])
    app.add_url_rule("/vehicles/<int:vehicle_id>", view_func=get_vehicle, methods=['GET'])
    app.add_url_rule("/vehicles/<int:vehicle_id>", view_func=update_vehicle, methods=['PUT'])
    app.add_url_rule("/vehicles/<int:vehicle_id>", view_func=delete_vehicle, methods=['DELETE'])
