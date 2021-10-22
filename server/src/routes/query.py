from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import or_

from src import db
from src.models.casm import Compound, Reaction, ReactionHistory, ReactionJsonSchema, ReactionSource, ReactionSchema, Pathway, PathwaySchema, ReactionHistory
from src.errors import handler

query_blueprint = Blueprint('query', __name__, url_prefix='/api/query')
query_blueprint.register_error_handler(handler.InvalidUsage,
                                       handler.handle_invalid_usage)


@query_blueprint.route('', methods=['POST'])
def reaction_query():
    query_keyword = request.values.get('query')
    query_type = request.values.get('type')

    query_result = get_query(query_keyword, query_type)

    if not query_result:
        errors = {'level': 'ERROR', 'message': 'No result for that query :('}
        raise handler.InvalidUsage(status_code=404, payload=errors)

    return jsonify(query_result)


def get_query(query_keyword, query_type):
    reaction_schema = ReactionSchema(many=True)

    result = None
    if query_type == 'name':
        query = Reaction.query.join(Reaction.identifiers).filter(
            ReactionSource.database_identifier.like(f'%{query_keyword}%'))
        query_result = query.all()

        result = reaction_schema.dump(query_result)

    elif query_type == 'metabolite':
        query = Reaction.query.filter(
            Reaction.formula.like(f'%{query_keyword}%'))
        query_result = query.all()
        result = reaction_schema.dump(query_result)

    elif query_type == 'metabolite_id':
        query = Compound.query.get(query_keyword)
        reactions = [reaction.reaction for reaction in query.reactions]

        result = reaction_schema.dump(reactions)

    elif query_type == 'pathway':
        pathway_schema = PathwaySchema(many=True)
        query = Pathway.query.filter(
            or_(Pathway.source_id.like(f'%{query_keyword}%'),
                Pathway.name.like(f'%{query_keyword}%')))
        query_result = query.all()

        result = pathway_schema.dump(query_result)

    return result


@query_blueprint.route('/reaction/<string:id>', methods=['GET'])
def reaction_id(id):
    reaction = Reaction.query.get(id)

    if reaction is None:
        errors = {'reaction': 'This reaction does not exist :('}
        raise handler.InvalidUsage(status_code=404, payload=errors)

    reaction_schema = ReactionJsonSchema()
    reaction_dump = reaction_schema.dump(reaction)

    return jsonify(reaction_dump)


@query_blueprint.route('/reaction/<string:id>/upload/<string:atom_id>',
                       methods=['POST'])
@jwt_required()
def reactionUpload(id, atom_id):
    user = current_user
    rxn_file = request.files['rxnFile'].read().decode()
    desc = request.values.get('description')

    history = ReactionHistory(reaction_id=atom_id,
                              file=rxn_file,
                              description=desc,
                              updated_by_id=user.id)
    db.session.add(history)
    db.session.commit()

    return jsonify({'message': 'Your update has been sent for review!'})


@query_blueprint.route('/metabolite/<string:id>', methods=['GET'])
def metaboliteId(id):
    metabolite = Compound.query.get(id)

    if metabolite is None:
        errors = {'metabolite': 'This metabolite does not exist :('}
        raise handler.InvalidUsage(status_code=404, payload=errors)

    metabolite_id = metabolite.id
    name = metabolite.name
    inchi = metabolite.inchi
    inchiShort = metabolite.inchi_short
    inchiKey = metabolite.inchi_key
    formula = metabolite.formula
    file = metabolite.file.decode("utf-8")
    elements = [{
        'qty': element.quantity,
        'id': element.element.id,
        'name': element.element.name,
        'symbol': element.element.symbol
    } for element in metabolite.elements]
    identifiers = [{
        'name': identifier.name,
        'identifier': identifier.database_identifier,
        'source': identifier.source.name
    } for identifier in metabolite.identifiers]
    reactions = [{
        'reactant': reaction.reactant,
        'formula': reaction.reaction.formula,
        'id': reaction.reaction.id
    } for reaction in metabolite.reactions.paginate(1, 20, False).items]

    result = {
        'id': metabolite_id,
        'name': name,
        'inchi': inchi,
        'inchiShort': inchiShort,
        'inchiKey': inchiKey,
        'formula': formula,
        'elements': elements,
        'identifiers': identifiers,
        'reactions': reactions,
        'file': file
    }

    return jsonify(result)


# @query_blueprint.route('/metabolite/<string:id>/upload', methods=['POST'])
# def metaboliteUpload(id):
#     mol_file = request.files['molfile'].read().decode()
#     compound = Compound.query.get(id)

#     compound.file = mol_file
#     db.session.commit()

#     return jsonify({'file': compound.file})
