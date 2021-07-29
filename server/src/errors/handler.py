"""Handler module responsible for the handling of exceptions."""

from typing import Any, List, Mapping

from flask import Response, jsonify


class InvalidUsage(Exception):
    """InvalidUsage handler that returns status code and payload.

    Args:
        status_code (int): Status code related to the error.
        payload (dict): Dictonary with messages depending on the error.
    """
    def __init__(self, status_code: int, payload: dict[str, str]):
        Exception.__init__(self)
        self.status_code = status_code
        self.payload = payload


class ExistingUser(InvalidUsage):
    """ExistingUser handler that returns a 400 error
    with a name error message.
    """
    def __init__(self):
        self.payload = {'name': 'User already exists'}
        self.status_code = 400

        super().__init__(self.status_code, self.payload)


class ExistingEmail(InvalidUsage):
    """ExistingEmail handler that returns a 400 error
    with a email error message.
    """
    def __init__(self):
        self.payload = {'email': 'There already is an account for that email'}
        self.status_code = 400

        super().__init__(self.status_code, self.payload)


class InvalidPassword(InvalidUsage):
    """InvalidPassword handler that returns a 400 error
    with a password error message.
    """
    def __init__(self):
        self.payload = {'password': 'Invalid password'}
        self.status_code = 400

        super().__init__(self.status_code, self.payload)


class InvalidUser(InvalidUsage):
    """InvalidUser handler that returns a 400 error
    with a name error message.
    """
    def __init__(self):
        self.payload = {'name': 'This name does not exist'}
        self.status_code = 400

        super().__init__(self.status_code, self.payload)


class InvalidId(InvalidUsage):
    """InvalidId handler that returns a 400 error
    with a invalid id error message.
    """
    def __init__(self):
        self.payload = {'message': 'Invalid id'}
        self.status_code = 400

        super().__init__(self.status_code, self.payload)


def handle_invalid_usage(error: InvalidUsage) -> Response:
    """Handles and returns base exceptions.

    Args:
        error (InvalidUsage): InvalidUsage object with the payload
        and status_code properties.

    Returns:
        Response: Flask Response object with JSON data
        containing status code and payload.
    """
    response: Response = jsonify(error.payload)
    response.status_code = error.status_code

    return response
