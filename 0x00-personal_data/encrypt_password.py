#!/usr/bin/env python3
"""A script that uses bcrypt to hash a password."""
import bcrypt


def hash_password(password: str) -> bytes:
    """
        A function that hashes a password.
        args:   password(str) the password to be hashed.
        return: A bytestring of the hashed password.
    """
    hashed_passwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_passwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
        A function that verifies that a password matches its hashed form.
        args:   hashed_password(bytes) the hashed password.
                password(str) the unhashed password.
        return: True if it matches else false.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
