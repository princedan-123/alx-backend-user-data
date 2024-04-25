#!/usr/bin/env python3
"""
Main file for test.
"""
import requests


def register_user(email: str, password: str) -> None:
    """A function that tests the register user endpoint."""
    data = {
        'email': email, 'password': password
        }
    response = requests.post('http://localhost:5000/users', data=data)
    assert response.status_code == 200 or response.status_code == 400
    try:
        result = response.json()
        assert result == {"email": email, "message": "user created"}
    except AssertionError:
        assert result == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """A function that tests a scenerio where a login attempts to
        login in with a wrong password.
    """
    data = {
        'email': email, 'password': password
        }
    response = requests.post('http://localhost:5000/sessions', data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """A function that tests if a user is logged in."""
    data = {
        'email': email, 'password': password
        }
    response = requests.post('http://localhost:5000/sessions', data=data)
    assert response.status_code == 200
    result = response.json()
    message = result.get('message')
    assert result == {"email": email, "message": "logged in"}
    return message


def profile_unlogged() -> None:
    """A function that tests if a user does not have a profile."""
    response = requests.get('http://localhost:5000/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """A function that tests if a user have a profile."""
    cookies = {'session_id': session_id}
    response = requests.get(
        'http://localhost:5000/profile', cookies=cookies
        )
    result = response.json()
    email = result.get('email')
    assert response.status_code == 200
    assert result == {"email": email}


def log_out(session_id: str) -> None:
    """A function that tests if a user is logged out."""
    cookies = {'session_id': session_id}
    response = requests.delete(
            'http://localhost:5000/sessions', cookies=cookies
            )
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """A function that tests the reset_password endpoint."""
    data = {'email': email}
    response = requests.post('http://localhost:5000/reset_password', data=data)
    result = response.json()
    reset_token = result.get('reset_token')
    assert response.status_code == {
        "email": email, "reset_token": reset_token
        }
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """A function that tests the updata_password endpoint."""
    data = {
        'email': email, 'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put('http://localhost:5000/reset_password', data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
