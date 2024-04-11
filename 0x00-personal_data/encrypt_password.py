#!/usr/bin/env python3
"""A script that uses bcrypt to hash a password."""
from bcrypt import gensalt, hashpw


def hash_password(password: str) -> bytes:
    """
        A function that hashes a password.
        args:   password(str) the password to be hashed.
        return: A bytestring of the hashed password.
    """
    hashed_passwd = hashpw(password.encode('utf-8'), gensalt())
    return hashed_passwd
