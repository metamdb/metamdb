"""Utility functions."""

from typing import Any


def is_empty(data: Any) -> bool:
    """Checks if argument is empty.

    Args:
        data (Any): To check if empty

    Returns:
        bool: Returns bool indicating if empty
    """
    if data is None or data == '' or data == 'null':
        return True

    return False
