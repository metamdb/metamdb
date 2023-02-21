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


@upload_blueprint.route('flux', methods=['POST', 'GET'])
def upload_flux_model() -> Response:
    """Route for processing of a flux mode.

    Returns:
        Response: JSON data containing each metabolite of the model.
    """
    # file: FileStorage = request.files['flux_file']
    # file_read = file.read().decode('utf-8')

    # model_data = json.loads(request.form['model'])
    # print(model_data)
    model_data = {
        'reactions': [{
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R1',
            'identifier':
            None,
            'index':
            1,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'G6P',
                'name': 'G6P',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdef',
                'metabolite': 'F6P',
                'name': 'F6P',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'F6P',
                    'name': 'F6P',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'G6P',
                    'name': 'G6P',
                    'qty': 1
                }]
            },
            'name':
            'R1',
            'reversible':
            True
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R2',
            'identifier':
            None,
            'index':
            2,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'F6P',
                'name': 'F6P',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdef',
                'metabolite': 'FBP',
                'name': 'FBP',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'FBP',
                    'name': 'FBP',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'F6P',
                    'name': 'F6P',
                    'qty': 1
                }]
            },
            'name':
            'R2',
            'reversible':
            False
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R3',
            'identifier':
            None,
            'index':
            3,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'FBP',
                'name': 'FBP',
                'reactant': 'substrate'
            }, {
                'mapping': 'cba',
                'metabolite': 'DHAP',
                'name': 'DHAP',
                'reactant': 'product'
            }, {
                'mapping': 'def',
                'metabolite': 'GAP',
                'name': 'GAP',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'DHAP',
                    'name': 'DHAP',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'GAP',
                    'name': 'GAP',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'FBP',
                    'name': 'FBP',
                    'qty': 1
                }]
            },
            'name':
            'R3',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R4',
            'identifier':
            None,
            'index':
            4,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'DHAP',
                'name': 'DHAP',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'GAP',
                'name': 'GAP',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'GAP',
                    'name': 'GAP',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'DHAP',
                    'name': 'DHAP',
                    'qty': 1
                }]
            },
            'name':
            'R4',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R5',
            'identifier':
            None,
            'index':
            5,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'GAP',
                'name': 'GAP',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'PG3',
                'name': 'PG3',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'PG3',
                    'name': 'PG3',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'GAP',
                    'name': 'GAP',
                    'qty': 1
                }]
            },
            'name':
            'R5',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R6',
            'identifier':
            None,
            'index':
            6,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'PG3',
                'name': 'PG3',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'PEP',
                'name': 'PEP',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'PEP',
                    'name': 'PEP',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'PG3',
                    'name': 'PG3',
                    'qty': 1
                }]
            },
            'name':
            'R6',
            'reversible':
            True
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R7',
            'identifier':
            None,
            'index':
            7,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'PEP',
                'name': 'PEP',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'PEP',
                    'name': 'PEP',
                    'qty': 1
                }]
            },
            'name':
            'R7',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R8',
            'identifier':
            None,
            'index':
            8,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'G6P',
                'name': 'G6P',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdef',
                'metabolite': 'PG6',
                'name': 'PG6',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'PG6',
                    'name': 'PG6',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'G6P',
                    'name': 'G6P',
                    'qty': 1
                }]
            },
            'name':
            'R8',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R9',
            'identifier':
            None,
            'index':
            9,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'PG6',
                'name': 'PG6',
                'reactant': 'substrate'
            }, {
                'mapping': 'bcdef',
                'metabolite': 'Ru5P',
                'name': 'Ru5P',
                'reactant': 'product'
            }, {
                'mapping': 'a',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Ru5P',
                    'name': 'Ru5P',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'PG6',
                    'name': 'PG6',
                    'qty': 1
                }]
            },
            'name':
            'R9',
            'reversible':
            False
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R10',
            'identifier':
            None,
            'index':
            10,
            'mappings': [[{
                'mapping': 'abcde',
                'metabolite': 'Ru5P',
                'name': 'Ru5P',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcde',
                'metabolite': 'X5P',
                'name': 'X5P',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'X5P',
                    'name': 'X5P',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Ru5P',
                    'name': 'Ru5P',
                    'qty': 1
                }]
            },
            'name':
            'R10',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R11',
            'identifier':
            None,
            'index':
            11,
            'mappings': [[{
                'mapping': 'abcde',
                'metabolite': 'Ru5P',
                'name': 'Ru5P',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcde',
                'metabolite': 'R5P',
                'name': 'R5P',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'R5P',
                    'name': 'R5P',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Ru5P',
                    'name': 'Ru5P',
                    'qty': 1
                }]
            },
            'name':
            'R11',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R12',
            'identifier':
            None,
            'index':
            12,
            'mappings': [[{
                'mapping': 'abcde',
                'metabolite': 'X5P',
                'name': 'X5P',
                'reactant': 'substrate'
            }, {
                'mapping': 'cde',
                'metabolite': 'GAP',
                'name': 'GAP',
                'reactant': 'product'
            }, {
                'mapping': 'ab',
                'metabolite': 'EC2',
                'name': 'EC2',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'GAP',
                    'name': 'GAP',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'EC2',
                    'name': 'EC2',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'X5P',
                    'name': 'X5P',
                    'qty': 1
                }]
            },
            'name':
            'R12',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R13',
            'identifier':
            None,
            'index':
            13,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'F6P',
                'name': 'F6P',
                'reactant': 'substrate'
            }, {
                'mapping': 'cdef',
                'metabolite': 'E4P',
                'name': 'E4P',
                'reactant': 'product'
            }, {
                'mapping': 'ab',
                'metabolite': 'EC2',
                'name': 'EC2',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'E4P',
                    'name': 'E4P',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'EC2',
                    'name': 'EC2',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'F6P',
                    'name': 'F6P',
                    'qty': 1
                }]
            },
            'name':
            'R13',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R14',
            'identifier':
            None,
            'index':
            14,
            'mappings': [[{
                'mapping': 'abcdefg',
                'metabolite': 'S7P',
                'name': 'S7P',
                'reactant': 'substrate'
            }, {
                'mapping': 'cdefg',
                'metabolite': 'R5P',
                'name': 'R5P',
                'reactant': 'product'
            }, {
                'mapping': 'ab',
                'metabolite': 'EC2',
                'name': 'EC2',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'R5P',
                    'name': 'R5P',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'EC2',
                    'name': 'EC2',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'S7P',
                    'name': 'S7P',
                    'qty': 1
                }]
            },
            'name':
            'R14',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R15',
            'identifier':
            None,
            'index':
            15,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'F6P',
                'name': 'F6P',
                'reactant': 'substrate'
            }, {
                'mapping': 'def',
                'metabolite': 'GAP',
                'name': 'GAP',
                'reactant': 'product'
            }, {
                'mapping': 'abc',
                'metabolite': 'EC3',
                'name': 'EC3',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'GAP',
                    'name': 'GAP',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'EC3',
                    'name': 'EC3',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'F6P',
                    'name': 'F6P',
                    'qty': 1
                }]
            },
            'name':
            'R15',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R16',
            'identifier':
            None,
            'index':
            16,
            'mappings': [[{
                'mapping': 'abcdefg',
                'metabolite': 'S7P',
                'name': 'S7P',
                'reactant': 'substrate'
            }, {
                'mapping': 'defg',
                'metabolite': 'E4P',
                'name': 'E4P',
                'reactant': 'product'
            }, {
                'mapping': 'abc',
                'metabolite': 'EC3',
                'name': 'EC3',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'E4P',
                    'name': 'E4P',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'EC3',
                    'name': 'EC3',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'S7P',
                    'name': 'S7P',
                    'qty': 1
                }]
            },
            'name':
            'R16',
            'reversible':
            True
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R17',
            'identifier':
            None,
            'index':
            17,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'PG6',
                'name': 'PG6',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdef',
                'metabolite': 'KDPG',
                'name': 'KDPG',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'KDPG',
                    'name': 'KDPG',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'PG6',
                    'name': 'PG6',
                    'qty': 1
                }]
            },
            'name':
            'R17',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R18',
            'identifier':
            None,
            'index':
            18,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'KDPG',
                'name': 'KDPG',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'product'
            }, {
                'mapping': 'def',
                'metabolite': 'GAP',
                'name': 'GAP',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'GAP',
                    'name': 'GAP',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'KDPG',
                    'name': 'KDPG',
                    'qty': 1
                }]
            },
            'name':
            'R18',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R19',
            'identifier':
            None,
            'index':
            19,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'substrate'
            }, {
                'mapping': 'bc',
                'metabolite': 'AcCoA',
                'name': 'AcCoA',
                'reactant': 'product'
            }, {
                'mapping': 'a',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'AcCoA',
                    'name': 'AcCoA',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }]
            },
            'name':
            'R19',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R20',
            'identifier':
            None,
            'index':
            20,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'OAA',
                'name': 'OAA',
                'reactant': 'substrate'
            }, {
                'mapping': 'ef',
                'metabolite': 'AcCoA',
                'name': 'AcCoA',
                'reactant': 'substrate'
            }, {
                'mapping': 'dcbfea',
                'metabolite': 'Cit',
                'name': 'Cit',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Cit',
                    'name': 'Cit',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'OAA',
                    'name': 'OAA',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AcCoA',
                    'name': 'AcCoA',
                    'qty': 1
                }]
            },
            'name':
            'R20',
            'reversible':
            False
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R21',
            'identifier':
            None,
            'index':
            21,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'Cit',
                'name': 'Cit',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdef',
                'metabolite': 'ICit',
                'name': 'ICit',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'ICit',
                    'name': 'ICit',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Cit',
                    'name': 'Cit',
                    'qty': 1
                }]
            },
            'name':
            'R21',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R22',
            'identifier':
            None,
            'index':
            22,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'ICit',
                'name': 'ICit',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcde',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }, {
                'mapping': 'f',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'ICit',
                    'name': 'ICit',
                    'qty': 1
                }]
            },
            'name':
            'R22',
            'reversible':
            True
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R23',
            'identifier':
            None,
            'index':
            23,
            'mappings': [[{
                'mapping': 'abcde',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'substrate'
            }, {
                'mapping': 'bcde',
                'metabolite': 'SucCoA',
                'name': 'SucCoA',
                'reactant': 'product'
            }, {
                'mapping': 'a',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'SucCoA',
                    'name': 'SucCoA',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }]
            },
            'name':
            'R23',
            'reversible':
            False
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R24',
            'identifier':
            None,
            'index':
            24,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'SucCoA',
                'name': 'SucCoA',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcd',
                'metabolite': 'Suc',
                'name': 'Suc',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Suc',
                    'name': 'Suc',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'SucCoA',
                    'name': 'SucCoA',
                    'qty': 1
                }]
            },
            'name':
            'R24',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R25',
            'identifier':
            None,
            'index':
            25,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'Suc',
                'name': 'Suc',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcd',
                'metabolite': 'Fum',
                'name': 'Fum',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Fum',
                    'name': 'Fum',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Suc',
                    'name': 'Suc',
                    'qty': 1
                }]
            },
            'name':
            'R25',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R26',
            'identifier':
            None,
            'index':
            26,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'Fum',
                'name': 'Fum',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcd',
                'metabolite': 'Mal',
                'name': 'Mal',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Mal',
                    'name': 'Mal',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Fum',
                    'name': 'Fum',
                    'qty': 1
                }]
            },
            'name':
            'R26',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R27',
            'identifier':
            None,
            'index':
            27,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'Mal',
                'name': 'Mal',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcd',
                'metabolite': 'OAA',
                'name': 'OAA',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'OAA',
                    'name': 'OAA',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Mal',
                    'name': 'Mal',
                    'qty': 1
                }]
            },
            'name':
            'R27',
            'reversible':
            True
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R28',
            'identifier':
            None,
            'index':
            28,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'Mal',
                'name': 'Mal',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'product'
            }, {
                'mapping': 'd',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Mal',
                    'name': 'Mal',
                    'qty': 1
                }]
            },
            'name':
            'R28',
            'reversible':
            False
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R29',
            'identifier':
            None,
            'index':
            29,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'PEP',
                'name': 'PEP',
                'reactant': 'substrate'
            }, {
                'mapping': 'd',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcd',
                'metabolite': 'OAA',
                'name': 'OAA',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'OAA',
                    'name': 'OAA',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'PEP',
                    'name': 'PEP',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }]
            },
            'name':
            'R29',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R30',
            'identifier':
            None,
            'index':
            30,
            'mappings': [[{
                'mapping': 'ab',
                'metabolite': 'AcCoA',
                'name': 'AcCoA',
                'reactant': 'substrate'
            }, {
                'mapping': 'ab',
                'metabolite': 'Ac',
                'name': 'Ac',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Ac',
                    'name': 'Ac',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'AcCoA',
                    'name': 'AcCoA',
                    'qty': 1
                }]
            },
            'name':
            'R30',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R31',
            'identifier':
            None,
            'index':
            31,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'DHAP',
                'name': 'DHAP',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'Glyc3P',
                'name': 'Glyc3P',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Glyc3P',
                    'name': 'Glyc3P',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'DHAP',
                    'name': 'DHAP',
                    'qty': 1
                }]
            },
            'name':
            'R31',
            'reversible':
            True
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R32',
            'identifier':
            None,
            'index':
            32,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'Glyc3P',
                'name': 'Glyc3P',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'Glyc',
                'name': 'Glyc',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Glyc',
                    'name': 'Glyc',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Glyc3P',
                    'name': 'Glyc3P',
                    'qty': 1
                }]
            },
            'name':
            'R32',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R33',
            'identifier':
            None,
            'index':
            33,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'Glyc',
                'name': 'Glyc',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'HPA',
                'name': 'HPA',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'HPA',
                    'name': 'HPA',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Glyc',
                    'name': 'Glyc',
                    'qty': 1
                }]
            },
            'name':
            'R33',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R34',
            'identifier':
            None,
            'index':
            34,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'HPA',
                'name': 'HPA',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'PDO',
                'name': 'PDO',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'PDO',
                    'name': 'PDO',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'HPA',
                    'name': 'HPA',
                    'qty': 1
                }]
            },
            'name':
            'R34',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R35',
            'identifier':
            None,
            'index':
            35,
            'mappings': [[{
                'mapping': 'abcde',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcde',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }]
            },
            'name':
            'R35',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R36',
            'identifier':
            None,
            'index':
            36,
            'mappings': [[{
                'mapping': 'abcde',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcde',
                'metabolite': 'Gln',
                'name': 'Gln',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Gln',
                    'name': 'Gln',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }]
            },
            'name':
            'R36',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R37',
            'identifier':
            None,
            'index':
            37,
            'mappings': [[{
                'mapping': 'abcde',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcde',
                'metabolite': 'Pro',
                'name': 'Pro',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Pro',
                    'name': 'Pro',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }]
            },
            'name':
            'R37',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R38',
            'identifier':
            None,
            'index':
            38,
            'mappings': [[{
                'mapping': 'abcde',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'f',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'substrate'
            }, {
                'mapping': 'ghijk',
                'metabolite': 'Gln',
                'name': 'Gln',
                'reactant': 'substrate'
            }, {
                'mapping': 'lmno',
                'metabolite': 'Asp',
                'name': 'Asp',
                'reactant': 'substrate'
            }, {
                'mapping': 'pq',
                'metabolite': 'AcCoA',
                'name': 'AcCoA',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdef',
                'metabolite': 'Arg',
                'name': 'Arg',
                'reactant': 'product'
            }, {
                'mapping': 'ghijk',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }, {
                'mapping': 'lmno',
                'metabolite': 'Fum',
                'name': 'Fum',
                'reactant': 'product'
            }, {
                'mapping': 'pq',
                'metabolite': 'Ac',
                'name': 'Ac',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Arg',
                    'name': 'Arg',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Fum',
                    'name': 'Fum',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Ac',
                    'name': 'Ac',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Gln',
                    'name': 'Gln',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Asp',
                    'name': 'Asp',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AcCoA',
                    'name': 'AcCoA',
                    'qty': 1
                }]
            },
            'name':
            'R38',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R39',
            'identifier':
            None,
            'index':
            39,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'OAA',
                'name': 'OAA',
                'reactant': 'substrate'
            }, {
                'mapping': 'efghi',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcd',
                'metabolite': 'Asp',
                'name': 'Asp',
                'reactant': 'product'
            }, {
                'mapping': 'efghi',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Asp',
                    'name': 'Asp',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'OAA',
                    'name': 'OAA',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }]
            },
            'name':
            'R39',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R40',
            'identifier':
            None,
            'index':
            40,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'Asp',
                'name': 'Asp',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcd',
                'metabolite': 'Asn',
                'name': 'Asn',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Asn',
                    'name': 'Asn',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Asp',
                    'name': 'Asp',
                    'qty': 1
                }]
            },
            'name':
            'R40',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R41',
            'identifier':
            None,
            'index':
            41,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'substrate'
            }, {
                'mapping': 'defgh',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'Ala',
                'name': 'Ala',
                'reactant': 'product'
            }, {
                'mapping': 'defgh',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Ala',
                    'name': 'Ala',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }]
            },
            'name':
            'R41',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R42',
            'identifier':
            None,
            'index':
            42,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'PG3',
                'name': 'PG3',
                'reactant': 'substrate'
            }, {
                'mapping': 'defgh',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'Ser',
                'name': 'Ser',
                'reactant': 'product'
            }, {
                'mapping': 'defgh',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Ser',
                    'name': 'Ser',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'PG3',
                    'name': 'PG3',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }]
            },
            'name':
            'R42',
            'reversible':
            False
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R43',
            'identifier':
            None,
            'index':
            43,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'Ser',
                'name': 'Ser',
                'reactant': 'substrate'
            }, {
                'mapping': 'ab',
                'metabolite': 'Gly',
                'name': 'Gly',
                'reactant': 'product'
            }, {
                'mapping': 'c',
                'metabolite': 'MEETHF',
                'name': 'MEETHF',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Gly',
                    'name': 'Gly',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'MEETHF',
                    'name': 'MEETHF',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Ser',
                    'name': 'Ser',
                    'qty': 1
                }]
            },
            'name':
            'R43',
            'reversible':
            True
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R44',
            'identifier':
            None,
            'index':
            44,
            'mappings': [[{
                'mapping': 'ab',
                'metabolite': 'Gly',
                'name': 'Gly',
                'reactant': 'substrate'
            }, {
                'mapping': 'a',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }, {
                'mapping': 'b',
                'metabolite': 'MEETHF',
                'name': 'MEETHF',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'MEETHF',
                    'name': 'MEETHF',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Gly',
                    'name': 'Gly',
                    'qty': 1
                }]
            },
            'name':
            'R44',
            'reversible':
            True
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R45',
            'identifier':
            None,
            'index':
            45,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'Thr',
                'name': 'Thr',
                'reactant': 'substrate'
            }, {
                'mapping': 'ab',
                'metabolite': 'Gly',
                'name': 'Gly',
                'reactant': 'product'
            }, {
                'mapping': 'cd',
                'metabolite': 'AcCoA',
                'name': 'AcCoA',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Gly',
                    'name': 'Gly',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AcCoA',
                    'name': 'AcCoA',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Thr',
                    'name': 'Thr',
                    'qty': 1
                }]
            },
            'name':
            'R45',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R46',
            'identifier':
            None,
            'index':
            46,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'Ser',
                'name': 'Ser',
                'reactant': 'substrate'
            }, {
                'mapping': 'de',
                'metabolite': 'AcCoA',
                'name': 'AcCoA',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'Cys',
                'name': 'Cys',
                'reactant': 'product'
            }, {
                'mapping': 'de',
                'metabolite': 'Ac',
                'name': 'Ac',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Cys',
                    'name': 'Cys',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Ac',
                    'name': 'Ac',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Ser',
                    'name': 'Ser',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AcCoA',
                    'name': 'AcCoA',
                    'qty': 1
                }]
            },
            'name':
            'R46',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R47',
            'identifier':
            None,
            'index':
            47,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'Asp',
                'name': 'Asp',
                'reactant': 'substrate'
            }, {
                'mapping': 'efg',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'substrate'
            }, {
                'mapping': 'hijkl',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'mnop',
                'metabolite': 'SucCoA',
                'name': 'SucCoA',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdgfe',
                'metabolite': 'LL_DAP',
                'name': 'LL_DAP',
                'reactant': 'product'
            }, {
                'mapping': 'hijkl',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }, {
                'mapping': 'mnop',
                'metabolite': 'Suc',
                'name': 'Suc',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'LL_DAP',
                    'name': 'LL_DAP',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Suc',
                    'name': 'Suc',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Asp',
                    'name': 'Asp',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'SucCoA',
                    'name': 'SucCoA',
                    'qty': 1
                }]
            },
            'name':
            'R47',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R48',
            'identifier':
            None,
            'index':
            48,
            'mappings': [[{
                'mapping': 'abcdefg',
                'metabolite': 'LL_DAP',
                'name': 'LL_DAP',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdef',
                'metabolite': 'Lys',
                'name': 'Lys',
                'reactant': 'product'
            }, {
                'mapping': 'g',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Lys',
                    'name': 'Lys',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'LL_DAP',
                    'name': 'LL_DAP',
                    'qty': 1
                }]
            },
            'name':
            'R48',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R49',
            'identifier':
            None,
            'index':
            49,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'Asp',
                'name': 'Asp',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcd',
                'metabolite': 'Thr',
                'name': 'Thr',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Thr',
                    'name': 'Thr',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Asp',
                    'name': 'Asp',
                    'qty': 1
                }]
            },
            'name':
            'R49',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R50',
            'identifier':
            None,
            'index':
            50,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'Asp',
                'name': 'Asp',
                'reactant': 'substrate'
            }, {
                'mapping': 'e',
                'metabolite': 'METHF',
                'name': 'METHF',
                'reactant': 'substrate'
            }, {
                'mapping': 'fgh',
                'metabolite': 'Cys',
                'name': 'Cys',
                'reactant': 'substrate'
            }, {
                'mapping': 'ijkl',
                'metabolite': 'SucCoA',
                'name': 'SucCoA',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcde',
                'metabolite': 'Met',
                'name': 'Met',
                'reactant': 'product'
            }, {
                'mapping': 'fgh',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'product'
            }, {
                'mapping': 'ijkl',
                'metabolite': 'Suc',
                'name': 'Suc',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Met',
                    'name': 'Met',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Suc',
                    'name': 'Suc',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Asp',
                    'name': 'Asp',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'METHF',
                    'name': 'METHF',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Cys',
                    'name': 'Cys',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'SucCoA',
                    'name': 'SucCoA',
                    'qty': 1
                }]
            },
            'name':
            'R50',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R51',
            'identifier':
            None,
            'index':
            51,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'substrate'
            }, {
                'mapping': 'def',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'substrate'
            }, {
                'mapping': 'ghijk',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcef',
                'metabolite': 'Val',
                'name': 'Val',
                'reactant': 'product'
            }, {
                'mapping': 'd',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }, {
                'mapping': 'ghijk',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Val',
                    'name': 'Val',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }]
            },
            'name':
            'R51',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R52',
            'identifier':
            None,
            'index':
            52,
            'mappings': [[{
                'mapping': 'ab',
                'metabolite': 'AcCoA',
                'name': 'AcCoA',
                'reactant': 'substrate'
            }, {
                'mapping': 'cde',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'substrate'
            }, {
                'mapping': 'fgh',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'substrate'
            }, {
                'mapping': 'ijklm',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'abdghe',
                'metabolite': 'Leu',
                'name': 'Leu',
                'reactant': 'product'
            }, {
                'mapping': 'c',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }, {
                'mapping': 'f',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }, {
                'mapping': 'ijklm',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Leu',
                    'name': 'Leu',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'AcCoA',
                    'name': 'AcCoA',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }]
            },
            'name':
            'R52',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R53',
            'identifier':
            None,
            'index':
            53,
            'mappings': [[{
                'mapping': 'abcd',
                'metabolite': 'Thr',
                'name': 'Thr',
                'reactant': 'substrate'
            }, {
                'mapping': 'efg',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'substrate'
            }, {
                'mapping': 'hijkl',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'abfcdg',
                'metabolite': 'Ile',
                'name': 'Ile',
                'reactant': 'product'
            }, {
                'mapping': 'e',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }, {
                'mapping': 'hijkl',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Ile',
                    'name': 'Ile',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Thr',
                    'name': 'Thr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }]
            },
            'name':
            'R53',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R54',
            'identifier':
            None,
            'index':
            54,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'PEP',
                'name': 'PEP',
                'reactant': 'substrate'
            }, {
                'mapping': 'def',
                'metabolite': 'PEP',
                'name': 'PEP',
                'reactant': 'substrate'
            }, {
                'mapping': 'ghij',
                'metabolite': 'E4P',
                'name': 'E4P',
                'reactant': 'substrate'
            }, {
                'mapping': 'klmno',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcefghij',
                'metabolite': 'Phe',
                'name': 'Phe',
                'reactant': 'product'
            }, {
                'mapping': 'd',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }, {
                'mapping': 'klmno',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Phe',
                    'name': 'Phe',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'PEP',
                    'name': 'PEP',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'E4P',
                    'name': 'E4P',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }]
            },
            'name':
            'R54',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R55',
            'identifier':
            None,
            'index':
            55,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'PEP',
                'name': 'PEP',
                'reactant': 'substrate'
            }, {
                'mapping': 'def',
                'metabolite': 'PEP',
                'name': 'PEP',
                'reactant': 'substrate'
            }, {
                'mapping': 'ghij',
                'metabolite': 'E4P',
                'name': 'E4P',
                'reactant': 'substrate'
            }, {
                'mapping': 'klmno',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcefghij',
                'metabolite': 'Tyr',
                'name': 'Tyr',
                'reactant': 'product'
            }, {
                'mapping': 'd',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }, {
                'mapping': 'klmno',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Tyr',
                    'name': 'Tyr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'PEP',
                    'name': 'PEP',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'E4P',
                    'name': 'E4P',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }]
            },
            'name':
            'R55',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R56',
            'identifier':
            None,
            'index':
            56,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'Ser',
                'name': 'Ser',
                'reactant': 'substrate'
            }, {
                'mapping': 'defgh',
                'metabolite': 'R5P',
                'name': 'R5P',
                'reactant': 'substrate'
            }, {
                'mapping': 'ijk',
                'metabolite': 'PEP',
                'name': 'PEP',
                'reactant': 'substrate'
            }, {
                'mapping': 'lmno',
                'metabolite': 'E4P',
                'name': 'E4P',
                'reactant': 'substrate'
            }, {
                'mapping': 'pqr',
                'metabolite': 'PEP',
                'name': 'PEP',
                'reactant': 'substrate'
            }, {
                'mapping': 'stuvw',
                'metabolite': 'Gln',
                'name': 'Gln',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcedklmnoj',
                'metabolite': 'Trp',
                'name': 'Trp',
                'reactant': 'product'
            }, {
                'mapping': 'i',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'product'
            }, {
                'mapping': 'fgh',
                'metabolite': 'GAP',
                'name': 'GAP',
                'reactant': 'product'
            }, {
                'mapping': 'pqr',
                'metabolite': 'Pyr',
                'name': 'Pyr',
                'reactant': 'product'
            }, {
                'mapping': 'stuvw',
                'metabolite': 'Glu',
                'name': 'Glu',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Trp',
                    'name': 'Trp',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'GAP',
                    'name': 'GAP',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Pyr',
                    'name': 'Pyr',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Glu',
                    'name': 'Glu',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Ser',
                    'name': 'Ser',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'R5P',
                    'name': 'R5P',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'PEP',
                    'name': 'PEP',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'E4P',
                    'name': 'E4P',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Gln',
                    'name': 'Gln',
                    'qty': 1
                }]
            },
            'name':
            'R56',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R57',
            'identifier':
            None,
            'index':
            57,
            'mappings': [[{
                'mapping': 'abcde',
                'metabolite': 'R5P',
                'name': 'R5P',
                'reactant': 'substrate'
            }, {
                'mapping': 'f',
                'metabolite': 'FTHF',
                'name': 'FTHF',
                'reactant': 'substrate'
            }, {
                'mapping': 'ghijk',
                'metabolite': 'Gln',
                'name': 'Gln',
                'reactant': 'substrate'
            }, {
                'mapping': 'lmno',
                'metabolite': 'Asp',
                'name': 'Asp',
                'reactant': 'substrate'
            }, {
                'mapping': 'edcbaf',
                'metabolite': 'His',
                'name': 'His',
                'reactant': 'product'
            }, {
                'mapping': 'ghijk',
                'metabolite': 'AKG',
                'name': 'AKG',
                'reactant': 'product'
            }, {
                'mapping': 'lmno',
                'metabolite': 'Fum',
                'name': 'Fum',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'His',
                    'name': 'His',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'AKG',
                    'name': 'AKG',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Fum',
                    'name': 'Fum',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'R5P',
                    'name': 'R5P',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'FTHF',
                    'name': 'FTHF',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Gln',
                    'name': 'Gln',
                    'qty': 1
                }, {
                    'elements': [],
                    'identifier': 'Asp',
                    'name': 'Asp',
                    'qty': 1
                }]
            },
            'name':
            'R57',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R58',
            'identifier':
            None,
            'index':
            58,
            'mappings': [[{
                'mapping': 'a',
                'metabolite': 'MEETHF',
                'name': 'MEETHF',
                'reactant': 'substrate'
            }, {
                'mapping': 'a',
                'metabolite': 'METHF',
                'name': 'METHF',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'METHF',
                    'name': 'METHF',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'MEETHF',
                    'name': 'MEETHF',
                    'qty': 1
                }]
            },
            'name':
            'R58',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R59',
            'identifier':
            None,
            'index':
            59,
            'mappings': [[{
                'mapping': 'a',
                'metabolite': 'MEETHF',
                'name': 'MEETHF',
                'reactant': 'substrate'
            }, {
                'mapping': 'a',
                'metabolite': 'FTHF',
                'name': 'FTHF',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'FTHF',
                    'name': 'FTHF',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'MEETHF',
                    'name': 'MEETHF',
                    'qty': 1
                }]
            },
            'name':
            'R59',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R60',
            'identifier':
            None,
            'index':
            60,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'Gluc.pre',
                'name': 'Gluc.pre',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdef',
                'metabolite': 'G6P',
                'name': 'G6P',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'G6P',
                    'name': 'G6P',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Gluc.pre',
                    'name': 'Gluc.pre',
                    'qty': 1
                }]
            },
            'name':
            'R60',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R61',
            'identifier':
            None,
            'index':
            61,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'Gluc.ext',
                'name': 'Gluc.ext',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdef',
                'metabolite': 'G6P',
                'name': 'G6P',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'G6P',
                    'name': 'G6P',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Gluc.ext',
                    'name': 'Gluc.ext',
                    'qty': 1
                }]
            },
            'name':
            'R61',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R62',
            'identifier':
            None,
            'index':
            62,
            'mappings': [[{
                'mapping': 'abcdef',
                'metabolite': 'Cit.ext',
                'name': 'Cit.ext',
                'reactant': 'substrate'
            }, {
                'mapping': 'abcdef',
                'metabolite': 'Cit',
                'name': 'Cit',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Cit',
                    'name': 'Cit',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Cit.ext',
                    'name': 'Cit.ext',
                    'qty': 1
                }]
            },
            'name':
            'R62',
            'reversible':
            False
        }, {
            'arrow':
            '<->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R63',
            'identifier':
            None,
            'index':
            63,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'Glyc.ext',
                'name': 'Glyc.ext',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'Glyc',
                'name': 'Glyc',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Glyc',
                    'name': 'Glyc',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Glyc.ext',
                    'name': 'Glyc.ext',
                    'qty': 1
                }]
            },
            'name':
            'R63',
            'reversible':
            True
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R64',
            'identifier':
            None,
            'index':
            64,
            'mappings': [[{
                'mapping': 'abc',
                'metabolite': 'PDO',
                'name': 'PDO',
                'reactant': 'substrate'
            }, {
                'mapping': 'abc',
                'metabolite': 'PDO.ext',
                'name': 'PDO.ext',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'PDO.ext',
                    'name': 'PDO.ext',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'PDO',
                    'name': 'PDO',
                    'qty': 1
                }]
            },
            'name':
            'R64',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R65',
            'identifier':
            None,
            'index':
            65,
            'mappings': [[{
                'mapping': 'ab',
                'metabolite': 'Ac',
                'name': 'Ac',
                'reactant': 'substrate'
            }, {
                'mapping': 'ab',
                'metabolite': 'Ac.ext',
                'name': 'Ac.ext',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'Ac.ext',
                    'name': 'Ac.ext',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'Ac',
                    'name': 'Ac',
                    'qty': 1
                }]
            },
            'name':
            'R65',
            'reversible':
            False
        }, {
            'arrow':
            '->',
            'conversion': {},
            'curated':
            'user',
            'database_identifier':
            'R66',
            'identifier':
            None,
            'index':
            66,
            'mappings': [[{
                'mapping': 'a',
                'metabolite': 'CO2',
                'name': 'CO2',
                'reactant': 'substrate'
            }, {
                'mapping': 'a',
                'metabolite': 'CO2.ext',
                'name': 'CO2.ext',
                'reactant': 'product'
            }]],
            'metabolites': {
                'product': [{
                    'elements': [],
                    'identifier': 'CO2.ext',
                    'name': 'CO2.ext',
                    'qty': 1
                }],
                'substrate': [{
                    'elements': [],
                    'identifier': 'CO2',
                    'name': 'CO2',
                    'qty': 1
                }]
            },
            'name':
            'R66',
            'reversible':
            False
        }, {
            'arrow': '->',
            'conversion': {},
            'curated': 'user',
            'database_identifier': 'R67',
            'identifier': None,
            'index': 67,
            'mappings': [],
            'metabolites': {
                'product': [],
                'substrate': []
            },
            'name': 'R67',
            'reversible': False
        }, {
            'arrow': '->',
            'conversion': {},
            'curated': 'user',
            'database_identifier': 'R68',
            'identifier': None,
            'index': 68,
            'mappings': [],
            'metabolites': {
                'product': [],
                'substrate': []
            },
            'name': 'R68',
            'reversible': False
        }]
    }
    # options = json.loads(request.form['options'])

    options = {
        'tracer': [{
            'name': 'Gluc.ext',
            'labeling': '100000',
            'purity': '1',
            'enrichment': '1'
        }],
        'targets': [{
            'value': 'Cit',
            'label': 'Cit'
        }, {
            'value': 'Mal',
            'label': 'Mal'
        }, {
            'value': 'Pyr',
            'label': 'Pyr'
        }, {
            'value': 'GAP',
            'label': 'GAP'
        }],
        'symmetry': [{
            'name': 'Suc',
            'symmetry': '4321'
        }, {
            'name': 'Fum',
            'symmetry': '4321'
        }],
        'ignore': []
    }

    tracers = [{
        k: float(v) if k in ['purity', 'enrichment'] else v
        for k, v in tracer.items()
    } for tracer in options['tracer']]

    targets = [target['value'] for target in options['targets']]
    symmetries = options['symmetry']
    ignore = [entry['value'] for entry in options['ignore']]

    aam_model = model.AtomMappingModel()._decode_metamdb(
        model_data['reactions'])

    # flux_model = [row.split(',') for row in file_read.split('\n') if row]
    # print(flux_model)
    flux_model = [['name', 'NET', 'EXCHANGE'], ['R1', '63.91', ''],
                  ['R2', '86.24', ''], ['R3', '86.24', '595.57'],
                  ['R4', '-41.07', '246.39'], ['R5', '56.28', '803000'],
                  ['R6', '54.72', '5571.9'], ['R7', '48.58', ''],
                  ['R8', '34.69', ''], ['R9', '34.55', ''],
                  ['R10', '22.39', '108.87'], ['R11', '12.16', ''],
                  ['R12', '22.39', '3125.7'], ['R13', '-11.03', '5.8'],
                  ['R14', '-11.36', '127.32'], ['R15', '-11.36', ''],
                  ['R16', '11.36', ''], ['R17', '0.14',
                                         ''], ['R18', '0.14', ''],
                  ['R19', '49.52', ''], ['R20', '46.58', ''],
                  ['R21', '46.85', '94.63'], ['R22', '46.85', '18500'],
                  ['R23', '45.89', ''], ['R24', '45.46', '451.66'],
                  ['R25', '45.89', '146.97'], ['R26', '46.22', '507000'],
                  ['R27', '43.07', '198.16'], ['R28', '3.15', ''],
                  ['R29', '5.44', '7.14'], ['R30', '-0.15', ''],
                  ['R31', '127.32', '300000'], ['R32', '127.32', ''],
                  ['R33', '129.3', ''], ['R34', '129.3', ''],
                  ['R35', '5.84', ''], ['R36', '0.6', ''], ['R37', '0.19', ''],
                  ['R38', '0.25', ''], ['R39', '1.63', ''], ['R40', '0.2', ''],
                  ['R41', '0.44', ''], ['R42', '1', ''],
                  ['R43', '0.56', '0.84'], ['R44', '0.04', '0.17'],
                  ['R45', '0', ''], ['R46', '0.21', ''], ['R47', '0.29', ''],
                  ['R48', '0.29', ''], ['R49', '0.46',
                                        ''], ['R50', '0.13', ''],
                  ['R51', '0.36', ''], ['R52', '0.38',
                                        ''], ['R53', '0.25', ''],
                  ['R54', '0.16', ''], ['R55', '0.12',
                                        ''], ['R56', '0.05', ''],
                  ['R57', '0.08', ''], ['R58', '0.13',
                                        ''], ['R59', '0.08', ''],
                  ['R60', '6.44', ''], ['R61', '92.35',
                                        ''], ['R62', '0.27', ''],
                  ['R63', '1.98', '45.83'], ['R64', '129.3', ''],
                  ['R65', '0.31', ''], ['R66', '176.29', ''],
                  ['R67', '0.89', ''], ['R68', '1.98', '']]

    aam_model = model.read_flux_model(flux_model, aam_model)

    sim = simulation.Simulation(aam_model)
    sim.initialize_substrates(tracers, ignore)
    sim.initialize_targets(targets)
    sim.initialize_symmetries(symmetries)
    sim.generate_emus()
    sim.calculate_mids()
    mids = sim.get_mids()

    return jsonify({'mids': mids})
