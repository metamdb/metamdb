"""Validate labeling simulation data."""

import json
from typing import Optional, Tuple, TypedDict

from src.validation.utils import is_empty


class Data(TypedDict):
    """
    Attr:
        element (str): Element as string.
        tracer (str): JSON encoded Tracer information with metabolite, purity, labeling keys.
        products (str): JSON encoded Products as list.
    """
    element: str
    tracer: str
    products: str


def validate_calculation(data: Data) -> Tuple[bool, Optional[dict[str, str]]]:
    """Validate calculation data.

    Args:
        data (Data): Data dict with element, tracer and products.

    Returns:
        bool: True if errors encountered during validation. Otherwise false.
        Optional[dict]: Error dictonary.
    """
    errors: dict[str, str] = {}

    if is_empty(data['element']):
        errors['element'] = 'Element field is required'

    if is_empty(data['tracer']):
        errors['tracer'] = 'A tracer is required'
    else:
        tracer = json.loads(data['tracer'])

        if is_empty(tracer['metabolite']):
            errors['metabolite'] = 'Metabolite field is required'

        if not all(char in '01' for char in tracer['labeling']):
            errors['labeling'] = "Labeling field can only contain 1's and 0's"

        if is_empty(tracer['labeling']):
            errors['labeling'] = 'Labeling field is required'

        if is_empty(tracer['purity']) or float(tracer['purity']) <= 0 or float(
                tracer['purity']) > 1:
            errors['purity'] = 'Purity can only be a float between 1 and 0'

        if is_empty(tracer['purity']):
            errors['purity'] = 'Purity field is required'

    if is_empty(data['products']):
        errors['products'] = 'Product field is required'

    if errors:
        return True, errors
    else:
        return False, None
