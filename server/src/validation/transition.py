"""Atom transition validation."""

from typing import Optional, Tuple, TypedDict

from src.validation.utils import is_empty


class Errors(TypedDict):
    element: str


class Data(TypedDict):
    """Validate transition arguments

    Attr:
        element (str): Element as string.
    """
    element: str


def validate_transition(data: Data) -> Tuple[bool, Optional[Errors]]:
    """Validate atom atom transition data. Returns True if errors are encountered.

    Args:
        data (Data): Dictonary with the key element.

    Returns:
        bool: Returns True if errors are encountered. Otherwise False.
        Optional[Errors]]: Returns error msg.
    """
    element = data['element']
    if is_empty(element):
        errors: Errors = {'element': 'Element field is required'}

        return True, errors

    return False, None
