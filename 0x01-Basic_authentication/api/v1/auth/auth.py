#!/usr/bin/env python3
"""A module to manage the API authentication."""
from flask import request
from typing import List, TypeVar


class Auth:
    """A class that manages the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            A public method that determines if a path needs authentication.
            args:   path(str) the path to be examined
                    excluded_paths(list) A list of paths that do not need
                    authentication.
            return: True if authentication is needed or False if not.
        """
        if path is None:
            return True
        if excluded_paths is None:
            return True
        elif len(excluded_paths) == 0:
            return True
        for url_path in excluded_paths:
            if url_path.endswith('*'):
                initial_segment = url_path[:-1]
                if path.startswith(initial_segment):
                    return False
        if not path.endswith('/'):
            path = path + '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """A public method that checks and returns the authorization header"""
        if request is None:
            return None
        authorization = request.headers.get('Authorization', None)
        if authorization is None:
            return None
        return authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """A public method."""
        return None
