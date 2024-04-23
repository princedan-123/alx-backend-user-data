#!/usr/bin/env python3
"""A module for authentication."""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    """A function that hashes and returns a hashed password."""
    byte_string = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(byte_string, bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """A method that generates and returns a unique string."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """A method that hashes a users password, before adding."""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound as error:
            hashed_password = _hash_password(password)
            registered_user = self._db.add_user(email, hashed_password)
            return registered_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        A method that validates a user
        args:   email(str): checks email
                password(str): checks password
        return: True if valid else False
        """
        try:
            user = self._db.find_user_by(email=email)
            password = password.encode('utf-8')
            if user:
                if bcrypt.checkpw(password, user.hashed_password):
                    return True
            return False
        except NoResultFound as error:
            return False
        except Exception as error:
            return False

    def create_session(self, email: str) -> str:
        """
        A method that generates a session id for a user for session based
        authentication.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                user.session_id = session_id
                return session_id
        except Exception:
            pass
