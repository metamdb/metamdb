from typing import Optional

from flask import Blueprint, json, jsonify, request
from src.errors import handler
from src.models.casm import Pathway, PathwayJsonSchema, PathwayReactionsSchema

pathways_blueprint = Blueprint('pathways',
                               __name__,
                               url_prefix='/api/pathways')
pathways_blueprint.register_error_handler(handler.InvalidUsage,
                                          handler.handle_invalid_usage)


@pathways_blueprint.route('', methods=['GET'])
def get_pathways():
    pathway_ids: Optional[str] = request.args.get('ids')
    if pathway_ids is None:
        raise handler.MissingRequiredQueryParameter(['ids'])
    elif not pathway_ids:
        raise handler.NoIdsGiven()

    split_ids = pathway_ids.split(',')
    pathways = []
    for pathway_id in split_ids:
        pathway = Pathway.query.get(pathway_id)
        if pathway:
            json_schema = PathwayJsonSchema()
            json_dump = json_schema.dump(pathway)
        else:
            json_dump = None

        pathways.append(json_dump)

    return jsonify({'pathways': pathways})


@pathways_blueprint.route('/<string:id>', methods=['GET'])
def get_pathway(id):
    pathway = Pathway.query.get(id)
    if not pathway:
        raise handler.InvalidId()

    json_schema = PathwayJsonSchema()
    json_dump = json_schema.dump(pathway)

    return jsonify(json_dump)


@pathways_blueprint.route('/<string:id>/reactions', methods=['GET'])
def get_pathway_reactions(id):
    pathway = Pathway.query.get(id)
    if not pathway:
        raise handler.InvalidId()

    json_schema = PathwayReactionsSchema()
    json_dump = json_schema.dump(pathway)

    return jsonify(json_dump)
