"""Flux model validation."""

from typing import Optional, Tuple, TypedDict


class Errors(TypedDict):
    file: str


ALLOWED_HEADERS = set(['FORWARD/REVERSE', 'NET/EXCHANGE'])


def validate_flux(first_header: str,
                  second_header: str) -> Tuple[bool, Optional[dict[str, str]]]:
    """Flux model validation.

    Args:
        first_header (string): A string of the first header of the csv file.
        second_header (string): A string of the second header of the csv file.

    Returns:
        bool: A boolean indicating errors with True.
        Optional[dict]: A dictonary of potential error messages.
    """
    header = first_header + '/' + second_header
    if header not in ALLOWED_HEADERS:
        errors = {
            'file':
            f'Flux model cant be identified, your header "{header}" is neither "FORWARD/REVERSE" nor "NET/EXCHANGE"'
        }

        return True, errors

    return False, None