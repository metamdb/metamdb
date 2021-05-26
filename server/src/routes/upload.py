"""Routes for the upload of model files."""

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage

from flask import Blueprint, Response, jsonify, request
from src.components.upload import reaction
from src.errors import handler
from src.errors.exception import (AtomMappingError,
                                  FluxModelIdentificationError,
                                  NoFluxTypeError)
from src.models import schema

upload_blueprint = Blueprint('upload', __name__, url_prefix='/api/upload')
upload_blueprint.register_error_handler(handler.InvalidUsage,
                                        handler.handle_invalid_usage)


@upload_blueprint.route('reaction', methods=['POST'])
def upload() -> Response:
    """Route for the processing of a reaction model.

    Returns:
        Response: JSON data containing the model data
    """
    file: FileStorage = request.files['reaction_file']
    file_read = file.read().decode('utf-8')

    model = reaction.ReactionModel()
    try:
        model.initialize_reactions(file_read)
    except (AtomMappingError, NoFluxTypeError,
            FluxModelIdentificationError) as error:
        error_message = error.args[0]
        raise handler.InvalidUsage(status_code=400,
                                   payload={'file': error_message})

    data = schema.ModelSchema().dump(model)

    return jsonify({'data': data})


@upload_blueprint.route('flux', methods=['POST'])
def upload_flux_model() -> Response:
    """Route for processing of a flux mode.

    Returns:
        Response: JSON data containing each metabolite of the model.
    """
    file: FileStorage = request.files['flux_file']
    file_read = file.read().decode('utf-8')

    model_data = request.form['model']
    model_schema = schema.ModelSchema()
    model = model_schema.load(json.loads(model_data))
    try:
        model.initialize_fluxes(file_read)
    except (NoFluxTypeError, FluxModelIdentificationError) as error:
        error_message = error.args[0]
        raise handler.InvalidUsage(status_code=400,
                                   payload={'flux_file': error_message})

    data = schema.ModelSchema(only=('reactions', )).dump(model)

    return jsonify({'data': data})
