from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import Inventory
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema
from utils.decorators import auth_required

# READ all inventory items
@inventory_bp.route("", methods=["GET"])
@auth_required("admin", "mechanic")
def get_inventory(user_id, role):
    items = db.session.query(Inventory).all()
    return jsonify(inventories_schema.dump(items)), 200

# CREATE new inventory item
@inventory_bp.route("", methods=["POST"])
@auth_required("admin")
def add_inventory(user_id, role):
    try:
        item = inventory_schema.load(request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    db.session.add(item)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during inventory creation"}), 500

    return jsonify(inventory_schema.dump(item)), 201

# UPDATE existing inventory item
@inventory_bp.route("/<int:item_id>", methods=["PUT"])
@auth_required("admin")
def update_inventory(user_id, role, item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    try:
        updated_item = inventory_schema.load(request.json, instance=item, partial=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during update"}), 500

    return jsonify(inventory_schema.dump(updated_item)), 200

# DELETE inventory item
@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
@auth_required("admin")
def delete_inventory(user_id, role, item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during deletion"}), 500

    return jsonify({"message": f"Inventory item {item_id} deleted"}), 200
