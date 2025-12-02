# utils/decorators.py
from functools import wraps
from flask import request, jsonify
from utils.auth import decode_token


def auth_required(*roles):
    """Decorator to enforce role-based access control for staff/admin users."""
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid token"}), 401

            token = auth_header.split(" ", 1)[1]
            try:
                payload = decode_token(token)
            except Exception:
                return jsonify({"error": "Invalid or expired token"}), 401

            user_id = payload.get("sub")
            role = payload.get("role")
            if roles and role not in roles:
                return jsonify({"error": "Forbidden"}), 403

            return fn(user_id, role, *args, **kwargs)
        return inner
    return wrapper

def token_required(fn):
    """Decorator to enforce customer token authentication."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            payload = decode_token(token)
        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401

        customer_id = payload.get("sub")
        return fn(customer_id, *args, **kwargs)
    return wrapper
