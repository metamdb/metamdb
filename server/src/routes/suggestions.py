from flask import Blueprint, jsonify, request
from src.errors import handler
from src.models.casm import Pathway, PathwayAutoCompleteSchema, ReactionAutoCompleteSchema, Compound, CompoundAutoCompleteSchema, ReactionSource
from sqlalchemy import or_

suggestions_blueprint = Blueprint('suggestions',
                                  __name__,
                                  url_prefix='/api/suggestions')
suggestions_blueprint.register_error_handler(handler.InvalidUsage,
                                             handler.handle_invalid_usage)


@suggestions_blueprint.route('/pathways', methods=['GET'])
def get_pathway_suggestions():
    q = request.args.get('q')
    pathways = Pathway.query.filter(
        or_(Pathway.name.like(f'{q}%'), Pathway.name.like(f'% {q}%'),
            Pathway.source_id.like(f'{q}%'),
            Pathway.source_id.like(f'% {q}%'))).order_by(
                Pathway.name.asc()).limit(10).all()

    json_schema = PathwayAutoCompleteSchema(many=True)
    json_dump = json_schema.dump(pathways)

    return jsonify(json_dump)


@suggestions_blueprint.route('/reactions', methods=['GET'])
def get_reactions_suggestions():
    q = request.args.get('q')
    reactions = ReactionSource.query.filter(
        or_(ReactionSource.database_identifier.like(f'{q}%'),
            ReactionSource.database_identifier.like(f'% {q}%'))).order_by(
                ReactionSource.database_identifier.asc()).limit(10).all()

    json_schema = ReactionAutoCompleteSchema(many=True)
    json_dump = json_schema.dump(reactions)

    return jsonify(json_dump)


@suggestions_blueprint.route('/metabolites', methods=['GET'])
def get_metabolites_suggestions():
    q = request.args.get('q')
    compounds = Compound.query.filter(Compound.name.like(f'{q}%')).order_by(
        Compound.name.asc()).limit(10).all()

    json_schema = CompoundAutoCompleteSchema(many=True)
    json_dump = json_schema.dump(compounds)

    return jsonify(json_dump)