from flask import request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError 
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

def create_customer():
    """POST /customers - Create a new customer."""
    try:
       # We catch the result directly as the model instance.
        new_customer = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check for email conflict using the instance attribute (.email), not .get()
    if _check_email_conflict(new_customer.email):
        return jsonify({"error": "Email already associated with an account"}), 409

    # The model instance is already created by customer_schema.load, 
    # so we add the instance directly, removing the redundant Customer(**...) line.
    db.session.add(new_customer)
    
    try:
        db.session.commit()
    except IntegrityError:
        # Rollback on database constraint violation (like a duplicate primary key or unexpected null)
        db.session.rollback()
        return jsonify({"error": "Database error during customer creation."}), 500
        
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

    # Use Marshmallow's built-in instance update functionality.
    # By passing 'instance=customer', the load method updates the existing customer 
    # object in place, removing the need for manual loops or .get().
    try:
        updated_customer = customer_schema.load(
            request.json, 
            instance=customer, 
            partial=True
        )
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check for email conflict using the attribute from the updated instance
    # We only check if 'email' was present in the request JSON to avoid false checks
    # if the schema returns the instance but the field wasn't loaded.
    new_email = request.json.get('email')

    if new_email is not None and new_email != customer.email:
        if _check_email_conflict(new_email, customer_id):
            # Rollback the in-place update if the email conflicts
            db.session.rollback()
            return jsonify({"error": "Email already associated with another account"}), 409

    # If the logic reaches here, the update is already staged in the 'customer' instance
    # due to the 'instance=customer' argument above.
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error during update."}), 500

    return customer_schema.jsonify(updated_customer), 200

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
        # This prevents crashes if the customer is referenced by another table (e.g., tickets)
        return jsonify({"error": "Cannot delete customer due to existing associated records."}), 409
        
    return jsonify({"message": f"Customer {customer_id} deleted successfully"}), 200

# Route Registration

def register_customer_routes(app):
    """Binds customer CRUD routes to the Flask application."""
    app.add_url_rule("/customers", view_func=create_customer, methods=['POST'])
    app.add_url_rule("/customers", view_func=get_customers, methods=['GET'])
    app.add_url_rule("/customers/<int:customer_id>", view_func=get_customer, methods=['GET'])
    app.add_url_rule("/customers/<int:customer_id>", view_func=update_customer, methods=['PUT'])
    app.add_url_rule("/customers/<int:customer_id>", view_func=delete_customer, methods=['DELETE'])