from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src import db
from src.models.casm import Compound, Reaction, ReactionSource, ReactionSchema
from src.components.mapping.aam import (generate_batch_aam,
                                        generate_batch_metabolite,
                                        generate_image_for_atom_transition)
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

    # print(result)
    return result


@query_blueprint.route('/reaction/<string:id>', methods=['GET'])
def reaction_id(id):
    reaction = Reaction.query.get(id)

    if reaction is None:
        errors = {'reaction': 'This reaction does not exist :('}
        raise handler.InvalidUsage(status_code=404, payload=errors)

    reaction_id = reaction.id
    formula = reaction.formula
    atom_transitions = {
        'file': reaction.file,
        'updated': reaction.updated,
        'updatedBy': reaction.updated_by,
        'updatedOn': reaction.updated_on,
        'id': reaction.id
    }
    identifiers = [{
        'identifier': identifier.database_identifier,
        'source': identifier.source.name
    } for identifier in reaction.identifiers]
    compounds = [{
        'reactant': compound.reactant,
        'name': compound.compound.name,
        'id': compound.compound.id
    } for compound in reaction.compounds]
    reaction_payload = {
        'id': reaction_id,
        'formula': formula,
        'atomTransitions': atom_transitions,
        'identifiers': identifiers,
        'compounds': compounds
    }

    return jsonify(reaction_payload)


# @query_blueprint.route('/reaction/<string:id>/generate', methods=['POST'])
# def generate_atom_transition(id):
#     reaction = Reaction.query.get(id)
#     atom_transition = generate_atom_transition_for_reaction(reaction)

#     result = {
#         'file': atom_transition.file,
#         'id': atom_transition.id,
#         'updated': atom_transition.updated,
#         'updated_by': atom_transition.updated_by,
#         'updated_on': atom_transition.updated_on
#     }

#     return jsonify(result)

# @query_blueprint.route('/reaction-batch', methods=['POST'])
# def generate_batch():
#     reactions = request.values.get('reactions')
#     reactions = reactions.split(',')
#     reactions = map(str.strip, reactions)
#     reactions = list(reactions)

#     reaction_ids = generate_batch_aam(reactions)

#     return jsonify({
#         'output': [{
#             'name': reaction,
#             'id': id
#         } for reaction, id in zip(reactions, reaction_ids)]
#     })

# @query_blueprint.route('/metabolite-batch', methods=['POST'])
# def generate_metabolite_batch():
#     metabolites = request.values.get('metabolites')
#     metabolites = metabolites.split(',')
#     metabolites = map(str.strip, metabolites)
#     metabolites = list(metabolites)

#     metabolite_ids = generate_batch_metabolite(metabolites)

#     return jsonify({
#         'output': [{
#             'name': metabolite,
#             'id': id
#         } for metabolite, id in zip(metabolites, metabolite_ids)]
#     })


@query_blueprint.route('/reaction/<string:id>/upload/<string:atomid>',
                       methods=['POST'])
@jwt_required
def reactionUpload(id, atomid):
    user = get_jwt_identity()

    rxnFile = request.files['rxnFile'].read().decode()
    desc = request.values.get('description')
    rxn = Reaction.query.get(atomid)

    rxn.file = rxnFile
    rxn.updated = 1
    rxn.updated_by = user['name']
    rxn.desc = desc
    db.session.commit()

    if desc != '':
        generate_image_for_atom_transition(id, rxnFile)

    result = {
        'file': rxn.file,
        'updated': rxn.updated,
        'updated_by': rxn.updated_by,
        'updated_on': rxn.updated_on,
        'desc': rxn.desc
    }

    return jsonify(result)


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


@query_blueprint.route('/metabolite/<string:id>/upload', methods=['POST'])
def metaboliteUpload(id):
    mol_file = request.files['molfile'].read().decode()
    compound = Compound.query.get(id)

    compound.file = mol_file
    db.session.commit()

    return jsonify({'file': compound.file})
