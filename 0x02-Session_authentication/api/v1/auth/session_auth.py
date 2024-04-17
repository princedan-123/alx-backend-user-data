#!/usr/bin/env python3
"""
A script that creates a class that will be used for session authentication.
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """A subclass of Auth that will be used for session authentication."""
    pass
