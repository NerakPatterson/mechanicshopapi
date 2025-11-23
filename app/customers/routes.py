from flask import request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from extensions import db
from models import Customer
from .schemas import customer_schema, customers_schema
from . import customer_bp
from flask import Blueprint, request
from extensions import limiter, cache, db
from models import Customer

customer_bp = Blueprint("customers", __name__)

@customer_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def list_customers():
    customers = Customer.query.all()
    return {"customers": [c.email for c in customers]}

@customer_bp.route("/", methods=["POST"])
@limiter.limit("10 per hour")
def create_customer():
    data = request.json
    new_customer = Customer(**data)
    db.session.add(new_customer)
    db.session.commit()
    return {"message": "Customer created"}, 201


# Helper function to check for email conflict
def _check_email_conflict(email, customer_id=None):
    query = select(Customer).where(Customer.email == email)
    existing_customer = db.session.execute(query).scalars().first()
    if existing_customer and (customer_id is None or existing_customer.id != customer_id):
        return True
    return False

@customer_bp.route("/", methods=["POST"])
def create_customer():
    """POST /customers - Create a new customer."""
    try:
        new_customer = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if _check_email_conflict(new_customer.email):
        return jsonify({"error": "Email already associated with an account"}), 409

    db.session.add(new_customer)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during customer creation."}), 500

    return customer_schema.jsonify(new_customer), 201

@customer_bp.route("/", methods=["GET"])
def get_customers():
    """GET /customers - Get all customers."""
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers)

@customer_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """GET /customers/<int:customer_id> - Get a single customer."""
    customer = db.session.get(Customer, customer_id)
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404

@customer_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """PUT /customers/<int:customer_id> - Update an existing customer."""
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    try:
        updated_customer = customer_schema.load(
            request.json,
            instance=customer,
            partial=True
        )
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_email = request.json.get("email")
    if new_email is not None and new_email != customer.email:
        if _check_email_conflict(new_email, customer_id):
            db.session.rollback()
            return jsonify({"error": "Email already associated with another account"}), 409

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error during update."}), 500

    return customer_schema.jsonify(updated_customer), 200

@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """DELETE /customers/<int:customer_id> - Delete a customer."""
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    db.session.delete(customer)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Cannot delete customer due to existing associated records."}), 409

    return jsonify({"message": f"Customer {customer_id} deleted successfully"}), 200
