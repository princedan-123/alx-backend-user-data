#!/usr/bin/env python3
"""
A script that creates a class that will be used for session authentication.
"""
import uuid
from api.v1.auth.auth import Auth


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
