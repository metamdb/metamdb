"""Routes for the upload of model files."""

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage

from flask import Blueprint, Response, jsonify, request
from src.components.upload import reaction, model
from src.components.calculation import simulation
from src.errors import handler
from src.errors.exception import (AtomMappingError,
                                  FluxModelIdentificationError,
                                  NoFluxTypeError, DeadEndError)
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


@upload_blueprint.route('flux', methods=['POST', 'GET'])
def upload_flux_model() -> Response:
    """Route for processing of a flux mode.

    Returns:
        Response: JSON data containing each metabolite of the model.
    """
    file: FileStorage = request.files['flux_file']
    file_read = file.read().decode('utf-8')
    # hola

    model_data = json.loads(request.form['model'])
    # print(model_data)
    options = json.loads(request.form['options'])
    print(options)
    tracers = [{
        k: float(v) if k in ['purity', 'enrichment'] else v
        for k, v in tracer.items()
    } for tracer in options['tracer']]

    targets = [target['value'] for target in options['targets']]
    symmetries = options['symmetry']
    ignore = [entry['value'] for entry in options['ignore']]

    aam_model = model.AtomMappingModel()._decode_metamdb(
        model_data['reactions'])

    print(file_read)
    if '\r\n' in file_read:
        flux_model = [row.split(',') for row in file_read.split('\r\n') if row]
    else:
        flux_model = [row.split(',') for row in file_read.split('\n') if row]

    print(flux_model)
    aam_model = model.read_flux_model(flux_model, aam_model)

    for name, reaction in aam_model.reactions.items():
        print('REACTION', reaction.__dict__)

    sim = simulation.Simulation(aam_model)
    sim.initialize_substrates(tracers, ignore)
    sim.initialize_targets(targets)
    sim.initialize_symmetries(symmetries)
    sim.generate_emus()
    sim.calculate_mids()
    mids = sim.get_mids()

    reactions = {'reactions': list(aam_model.reactions.values())}
    model_reactions = schema.AtomMappingModelSchema().dump(
        reactions)['reactions']

    return jsonify({'mids': mids, 'model': model_reactions})
