#!/usr/bin/env python3
"""A module that handles all routes for the Session authentication."""
import os
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False
    )
def login_session():
    """A view for session logins."""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception as e:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        valid = user.is_valid_password(password)
        if valid:
            from api.v1.app import auth
            session_id = auth.create_session(user.get('id'))
            cookie_name = os.getenv('SESSION_NAME')
            user_dict = user.to_json()
            response = jsonify(user_dict)
            response.set_cookie(cookie_name, session_id)
            return response
        return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route(
    'auth_session/logout', methods=['DELETE'], strict_slashes=False
    )
def logout():
    """An endpoint that implementes logout."""
    from api.v1.app import auth
    logged_out = auth.destroy_session(request)
    if not logged_out:
        abort(404)
    return jsonify({}), 200
