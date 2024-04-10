#!/usr/bin/env python3
"""A script that obfuscates sensitive data."""
from typing import List
import re


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """
        A function that obsfucates Personal identifiable information.
        args:   fields(list) a list of fields that needs to be obfuscated.
                redaction(string) a string that redacts sensitive data.
                message(string) the log line.
                separator(string) the character that separates each fields.
        return: A string is returned.

    """
    for field in message.split(separator):
        new_field = field.split('=')
        if new_field[0] in fields:
            message = re.sub(new_field[1], redaction, message)
    return message
