#!/usr/bin/env python3
"""A script that obfuscates sensitive data."""
from typing import List, Sequence
import re
import logging
import mysql.connector
import os

PII_FIELDS = ('name', 'email', 'ssn', 'phone', 'password')


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
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """A function that returns a connection object to a database."""
    host: str = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    password: str = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    user_name: str = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    database: str = os.environ.get('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(
        host=host, password=password, username=user_name,
        database=database
        )
    return connection


def main() -> None:
    """A function that queries a database and prints the result."""
    #  get logger object
    logger = get_logger()
    #  retrieve rows from a table in a database
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        message_field = (
            'name', 'email', 'phone', 'ssn',
            'password', 'ip', 'last_login',
            'user_agent'
            )
        log_message = ''
        for row in rows:
            field_and_value = zip(message_field, row)
            for data in field_and_value:
                field, value = data
                log_message += f'{field}={value};'
            logger.info(log_message)
        connection.close()


if __name__ == '__main__':
    main()
