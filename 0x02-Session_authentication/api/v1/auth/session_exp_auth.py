#!/usr/bin/env python3
"""A module that adds expiration to session id."""
import os
import uuid
import datetime
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """An implementation of a session with expiration time."""
    def __init__(self):
        """An initialization method."""
        try:
            session_duration = int(os.getenv('SESSION_DURATION', None))
        except Exception as error:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """A method that creates a session id for a user."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id, 'created_at': datetime.datetime.now()
            }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """A method that retrieves user id based on session id."""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get('user_id')
        if 'created_at' not in self.user_id_by_session_id.get(session_id):
            return None
        create = self.user_id_by_session_id.get(session_id).get('created_at')
        expiration_time = create + datetime.timedelta(
            seconds=self.session_duration
            )
        if expiration_time < datetime.datetime.now():
            return None
        return self.user_id_by_session_id.get(session_id).get('user_id')
