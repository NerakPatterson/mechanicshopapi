from flask import request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from extensions import db
from models import User, Role
from .schemas import user_schema, users_schema, login_schema
from . import user_bp
from utils.auth import encode_token
from utils.decorators import token_required, auth_required
from werkzeug.security import check_password_hash

@user_bp.route("/login", methods=["POST"])
def login():
    """POST /users/login - Authenticate staff (admin/mechanic) and return JWT token."""
    try:
        creds = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user = db.session.query(User).filter_by(email=creds.email).first()
    if not user or not check_password_hash(user.password, creds.password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Attach role name to token payload
    role_name = user.role.role_name if user.role else None
    token = encode_token(user.id, role=role_name)
    return jsonify({"token": token, "role": role_name}), 200

@user_bp.route("/", methods=["GET"])
@auth_required("admin")   # only admins can list all users
def get_users(user_id, role):
    """GET /users - List all users (admin only)."""
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return jsonify(users_schema.dump(users)), 200

@user_bp.route("/<int:user_id>", methods=["GET"])
@auth_required("admin", "mechanic")
def get_user(requester_id, role, user_id):
    """GET /users/<id> - Get a single user (admin/mechanic)."""
    user = db.session.get(User, user_id)
    if user:
        return jsonify(user_schema.dump(user)), 200
    return jsonify({"error": "User not found"}), 404

@user_bp.route("/<int:user_id>", methods=["DELETE"])
@auth_required("admin")   # only admins can delete
def delete_user(requester_id, role, user_id):
    """DELETE /users/<id> - Delete a user (admin only)."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error during deletion."}), 500

    return jsonify({"message": f"User {user_id} deleted by admin (user {requester_id})"}), 200
