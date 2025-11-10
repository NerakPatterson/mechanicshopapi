from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from extensions import db
from models import Customer
from schemas import customer_schema, customers_schema 

# Helper function to check for email conflict
def _check_email_conflict(email, customer_id=None):
    query = select(Customer).where(Customer.email == email)
    existing_customer = db.session.execute(query).scalars().first()
    
    # Check if the email exists for a DIFFERENT customer
    if existing_customer and (customer_id is None or existing_customer.id != customer_id):
        return True
    return False

# --- API Endpoints defined at Module Level (Fixes Pylance visibility) ---

def create_customer():
    """POST /customers - Create a new customer."""
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if _check_email_conflict(customer_data.get('email')):
        return jsonify({"error": "Email already associated with an account"}), 409

    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

def get_customers():
    """GET /customers - Get all customers."""
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers)

def get_customer(customer_id):
    """GET /customers/<int:customer_id> - Get a single customer."""
    customer = db.session.get(Customer, customer_id)
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404

def update_customer(customer_id):
    """PUT /customers/<int:customer_id> - Update an existing customer."""
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_email = customer_data.get('email')
    if new_email and new_email != customer.email:
        if _check_email_conflict(new_email, customer_id):
            return jsonify({"error": "Email already associated with another account"}), 409

    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

def delete_customer(customer_id):
    """DELETE /customers/<int:customer_id> - Delete a customer."""
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {customer_id} deleted successfully"}), 200

# -------------------------------------------------------------------
# Route Registration
# -------------------------------------------------------------------

def register_customer_routes(app):
    """Binds customer CRUD routes to the Flask application."""
    app.add_url_rule("/customers", view_func=create_customer, methods=['POST'])
    app.add_url_rule("/customers", view_func=get_customers, methods=['GET'])
    app.add_url_rule("/customers/<int:customer_id>", view_func=get_customer, methods=['GET'])
    app.add_url_rule("/customers/<int:customer_id>", view_func=update_customer, methods=['PUT'])
    app.add_url_rule("/customers/<int:customer_id>", view_func=delete_customer, methods=['DELETE'])