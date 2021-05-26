"""Routes for the generation of atom mapping models."""

from flask import Blueprint, jsonify, request, Response

from src.errors import handler
from src.validation.transition import validate_transition
from src.models.casm import Compound

transition_blueprint = Blueprint('transition',
                                 __name__,
                                 url_prefix='/api/transition')
transition_blueprint.register_error_handler(handler.InvalidUsage,
                                            handler.handle_invalid_usage)


@transition_blueprint.route('', methods=['POST'])
def transition() -> Response:
    data = request.form.to_dict()

    return jsonify({'atomMappingModel': 'test'})
