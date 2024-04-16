#!/usr/bin/env python3
"""A module that implements BasicAuthentication."""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """A public method that decodes a base64 string."""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            byte_string = base64.b64decode(base64_authorization_header)
            string = byte_string.decode('utf-8')
            return string
        except Exception as error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """A public method that extracts fields from a decoded base64."""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        fields = decoded_base64_authorization_header.split(':')
        return tuple(fields)
