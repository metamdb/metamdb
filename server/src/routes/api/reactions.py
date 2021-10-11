from typing import Optional

from flask import Blueprint, json, jsonify, request
from src.errors import handler
from src.models.casm import Reaction, ReactionJsonSchema

reactions_blueprint = Blueprint('reactions',
                                __name__,
                                url_prefix='/api/reactions')
reactions_blueprint.register_error_handler(handler.InvalidUsage,
                                           handler.handle_invalid_usage)


@reactions_blueprint.route('', methods=['GET'])
def get_reactions():
    reaction_ids: Optional[str] = request.args.get('ids')
    if not reaction_ids:
        raise handler.InvalidId()

    split_ids = reaction_ids.split(',')
    reactions = []
    for reaction_id in split_ids:
        reaction = Reaction.query.get(reaction_id)
        if reaction:
            json_schema = ReactionJsonSchema()
            json_dump = json_schema.dump(reaction)
        else:
            json_dump = None

        reactions.append(json_dump)

    return jsonify({'reactions': reactions})


@reactions_blueprint.route('/<string:id>', methods=['GET'])
def get_reaction(id):
    reaction = Reaction.query.get(id)
    if not reaction:
        raise handler.InvalidId()

    json_schema = ReactionJsonSchema()
    json_dump = json_schema.dump(reaction)

    return jsonify(json_dump)
