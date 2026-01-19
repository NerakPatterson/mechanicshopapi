from flask import request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from extensions import db
from models import User
from .schemas import user_schema, users_schema, login_schema
from . import user_bp
from utils.auth import encode_token
from utils.decorators import auth_required


# REGISTER USER
@user_bp.route("/register", methods=["POST"])
def register():
    """POST /users/register - Create a new user."""
    data = request.json or {}

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    # ⭐ Idempotent behavior FIRST ⭐
    existing = db.session.query(User).filter_by(email=email).first()
    if existing:
        return jsonify(user_schema.dump(existing)), 200

    # Validate fields
    if not email or not password or not role:
        return jsonify({"error": "Missing required fields"}), 400

    if role not in ["admin", "mechanic", "customer"]:
        return jsonify({"error": "Invalid role"}), 400

    user = User(email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 400

    return jsonify(user_schema.dump(user)), 201


# LOGIN USER
@user_bp.route("/login", methods=["POST"])
def login():
    """POST /users/login - Authenticate and return JWT."""
    try:
        creds = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user = db.session.query(User).filter_by(email=creds["email"]).first()
    if not user or not user.check_password(creds["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = encode_token(user.id, role=user.role)

    return jsonify({
        "token": token,
        "role": user.role
    }), 200


# GET ALL USERS (ADMIN ONLY)
@user_bp.route("", methods=["GET"])
@auth_required("admin")
def get_users(requester_id, role):
    """GET /users - List all users (admin only)."""
    users = db.session.execute(select(User)).scalars().all()
    return jsonify(users_schema.dump(users)), 200


# GET SINGLE USER (ADMIN + MECHANIC)
@user_bp.route("/<int:user_id>", methods=["GET"])
@auth_required("admin", "mechanic")
def get_user(requester_id, role, user_id):
    """GET /users/<id> - Get a single user."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user_schema.dump(user)), 200


# UPDATE USER (ADMIN ONLY)
@user_bp.route("/<int:user_id>", methods=["PUT"])
@auth_required("admin")
def update_user(requester_id, role, user_id):
    """PUT /users/<id> - Update a user (admin only)."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json or {}

    if "email" in data:
        user.email = data["email"]

    if "role" in data:
        if data["role"] not in ["admin", "mechanic", "customer"]:
            return jsonify({"error": "Invalid role"}), 400
        user.role = data["role"]

    if "password" in data:
        user.set_password(data["password"])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 400

    return jsonify({
        "message": f"User {user_id} updated by admin (user {requester_id})",
        "user": user_schema.dump(user)
    }), 200


# DELETE USER (ADMIN ONLY)
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@auth_required("admin")
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

    return jsonify({
        "message": f"User {user_id} deleted by admin (user {requester_id})"
    }), 200