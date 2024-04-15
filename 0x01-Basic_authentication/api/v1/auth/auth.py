#!/usr/bin/env python3
"""A module to manage the API authentication."""
from flask import request
from typing import List, TypeVar


class Auth:
    """A class that manages the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A public method."""
        return False

    def authorization_header(self, request=None) -> str:
        """A public method."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """A public method."""
        return None
