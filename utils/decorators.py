from functools import wraps
from flask import request, jsonify, current_app
from utils.auth import decode_token


def auth_required(*roles):
    """Decorator to enforce role-based access control for staff/admin users."""
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):

            # BYPASS AUTH IN TEST MODE
            if current_app.config.get("TESTING"):
                return fn(None, None, *args, **kwargs)

            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid token"}), 401

            token = auth_header.split(" ", 1)[1]
            payload = decode_token(token)

            if isinstance(payload, dict) and "error" in payload:
                return jsonify(payload), 401

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

        # DO NOT bypass token auth in tests
        # Customers must provide a token even in TESTING mode

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401

        token = auth_header.split(" ", 1)[1]
        payload = decode_token(token)

        if isinstance(payload, dict) and "error" in payload:
            return jsonify(payload), 401

        customer_id = payload.get("sub")
        return fn(customer_id, *args, **kwargs)

    return wrapper