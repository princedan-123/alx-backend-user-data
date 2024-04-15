#!/usr/bin/env python3
"""A module that implements BasicAuthentication."""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """A subclass of Auth."""
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """
            A public method that extracts the encoded portion of Authorization
            request header.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if 'Basic ' not in authorization_header:
            return None
        encoded_portion = authorization_header[6:]
        return encoded_portion
