#!/usr/bin/env python3
"""A simple flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


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
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError as error:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """A simple login in implementation"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": "<user email>", "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        return abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
