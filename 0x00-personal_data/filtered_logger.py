#!/usr/bin/env python3
"""A script that obfuscates sensitive data."""
from typing import List, Sequence
import re
import logging

PII_FIELDS = ('name', 'email', 'ip', 'phone', 'password')


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


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """An initialization method that initializes the class instance."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """A method that formats the log record."""
        return filter_datum(
            self.fields, self.REDACTION, super().format(record), self.SEPARATOR
            )


def get_logger() -> logging.Logger:
    """A function that creates a logger object."""
    user_data = logging.getLogger('user_data')
    user_data.setLevel(logging.INFO)
    user_data.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_data.addHandler(stream_handler)
    return user_data
