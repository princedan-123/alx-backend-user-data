#!/usr/bin/env python3
"""A simple flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from db import DB

app = Flask(__name__)
AUTH = Auth()
db = DB()


@app.route('/')
def root():
    """The landing page."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    An endpoint that implements the register_user method
    which registers a user.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError as error:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """A simple login in implementation"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        return abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """A route that implements a simple log out."""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    try:
        user = db.find_user_by(session_id=session_id)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except Exception:
        abort(403)


@app.route('/profile', strict_slashes=False)
def profile():
    """A route for acessing user profile."""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    try:
        user = db.find_user_by(session_id=session_id)
        return jsonify({"email": user.email}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """A route that resets a users password."""
    email = request.form.get('email')
    try:
        user = db.find_user_by(email=email)
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify(
            {"email": email, "reset_token": reset_token}
            ), 200

    except Exception:
        raise abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    A route that updates a user's password in case of forgotten password.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify(
            {"email": email, "message": "Password updated"}
            ), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
