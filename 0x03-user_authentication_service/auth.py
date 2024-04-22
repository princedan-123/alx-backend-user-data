#!/usr/bin/env python3
"""A module for authentication."""
import bcrypt


def _hash_password(password: str) -> bytes:
    """A function that hashes and returns a hashed password."""
    byte_string = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(byte_string, bcrypt.gensalt())
    return hashed_password
