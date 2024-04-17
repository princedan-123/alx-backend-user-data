#!/usr/bin/env python3
"""
A script that creates a class that will be used for session authentication.
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """A subclass of Auth that will be used for session authentication."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """A public method that creates a session_id for a user_id."""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """A public method that retrieves user_id based on session_id. """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)
    
    def current_user(self, request=None):
        """A method that retrieves a user based on its id."""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(str(user_id))