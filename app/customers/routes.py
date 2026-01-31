from flask import request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from extensions import db, limiter
from models import Customer, ServiceTicket, Vehicle
from .schemas import customer_schema, customers_schema
from . import customer_bp
from utils.decorators import auth_required, token_required   # unified + token decorator

# Helper function to check for email conflict
def _check_email_conflict(email, customer_id=None):
    query = select(Customer).where(Customer.email == email)
    existing_customer = db.session.execute(query).scalars().first()
    if existing_customer and (customer_id is None or existing_customer.id != customer_id):
        return True
    return False

@customer_bp.route("/my-tickets", methods=["GET"])
@token_required
def my_tickets(customer_id):
    """GET /my-tickets - Return tickets for the authenticated customer."""
    tickets = (
        db.session.query(ServiceTicket)
        .join(Vehicle, Vehicle.id == ServiceTicket.vehicle_id)
        .filter(Vehicle.customer_id == customer_id)
        .all()
    )
    return jsonify([{
        "id": t.id,
        "date": t.date.isoformat(),
        "description": t.description,
        "status": t.status,
        "cost": str(t.cost)
    } for t in tickets]), 200

@customer_bp.route("", methods=["GET"])
def get_customers():
    """GET /customers - Paginated list of customers."""
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    query = select(Customer)
    customers = db.session.execute(query).scalars().all()

    start = (page - 1) * per_page
    end = start + per_page
    paginated = customers[start:end]

    return jsonify(customers_schema.dump(paginated)), 200

@customer_bp.route("", methods=["POST"])
@auth_required("admin", "mechanic")   # admins and mechanics allowed
@limiter.limit("10 per hour")
def create_customer(user_id, role):
    """POST /customers - Create a new customer (admin/mechanic only)."""
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

    return jsonify({
        "message": f"Customer created by {role} (user {user_id})",
        "customer": customer_schema.dump(new_customer)
    }), 201

@customer_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """GET /customers/<customer_id> - Get a single customer."""
    customer = db.session.get(Customer, customer_id)
    if customer:
        return jsonify(customer_schema.dump(customer)), 200
    return jsonify({"error": "Customer not found."}), 404

@customer_bp.route("/<int:customer_id>", methods=["PUT"])
@auth_required("admin", "mechanic")   # restrict updates
def update_customer(user_id, role, customer_id):
    """PUT /customers/<customer_id> - Update an existing customer (admin/mechanic only)."""
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
    if new_email and new_email != customer.email:
        if _check_email_conflict(new_email, customer_id):
            db.session.rollback()
            return jsonify({"error": "Email already associated with another account"}), 409

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error during update."}), 500

    return jsonify({
        "message": f"Customer updated by {role} (user {user_id})",
        "customer": customer_schema.dump(updated_customer)
    }), 200

@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
@auth_required("admin")   # only admins can delete
def delete_customer(user_id, role, customer_id):
    """DELETE /customers/<customer_id> - Delete a customer (admin only)."""
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    db.session.delete(customer)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Cannot delete customer due to existing associated records."}), 409

    return jsonify({"message": f"Customer {customer_id} deleted by admin (user {user_id})"}), 200