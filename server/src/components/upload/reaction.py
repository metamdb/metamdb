"""This module implements functionality for reaction models"""
import csv
import logging
import re
from typing import Any, List, Optional, Tuple, Union, TYPE_CHECKING
from src.models.casm import Reaction as CasmReaction
if TYPE_CHECKING:
    from typings.casm.reaction import AtomBlockTyping, AtomTransitionTyping, MappingTyping, MetabolitesTyping, MetaboliteTyping
from src.errors.exception import FluxModelIdentificationError, MissingAtomMappingError, NoFluxTypeError

from src.components.upload import element as ele
from src.components.calculation.emu import Metabolite
from src.errors import handler, loggers
from src.models import casm
from src.validation import flux_upload

VALID_REACTION_IDENTIFIER = re.compile(
    r'''
    ([^\s\+]\S*) # reaction name
    \s* # whitespace between name and identifier
    (?:[(\[]([\S]*)[)\]])? # any non-whitespace character in [/( brackets
    ''', re.VERBOSE)

VALID_REACTION_IDENTIFIER_NEW = re.compile(
    r'''
    (?P<const>\d{1,3}\s)?(?P<name>[^\s\+]\S*)(?:\s\((?P<aam>[\S]*)\)\s*|\s\[(?P<id>[\S]*)\]\s*)(?:\s*\((?P<aam2>[\S]*)\)\s*|\s*\[(?P<id2>[\S]*)\]\s*)?
    ''', re.VERBOSE)

REVERSIBLE = ['↔', '<=>', '<->', '<>']
PRODUCTS_RIGHT = ['→', '->', '-->', '>']
PRODUCTS_LEFT = ['←', '<-', '<--', '<']

REACTION_NAME = re.compile(r'([^\s\+]\S*)\s*(?:[(\[](?:[\S]*)[)\]])?')

METABOLITES = {}


class ReactionModel():
    """Establishes the reaction model, detecting reactions.

    file (): Uploaded csv file.

    reaction ():

    metabolites ():

    elements ():

    flux_model ():
    """
    def __init__(self):
        self.file = None
        self.reactions = None
        self.metabolites: dict[Union[int, str], Metabolite] = {}
        self.elements = None
        self.flux_model = False

    def initialize_fluxes(self, file):
        content = [{
            'reaction': row[0],
            'first_flux': row[1],
            'second_flux': row[2]
        } for row in csv.reader(file.splitlines())]

        header, data = content[0], content[1:]

        first_header, second_header = header['first_flux'].strip().upper(
        ), header['second_flux'].strip().upper()

        is_error, errors = flux_upload.validate_flux(first_header,
                                                     second_header)

        if is_error and errors is not None:
            raise handler.InvalidUsage(status_code=400, payload=errors)

        flux_type = '_'.join([first_header, second_header])

        for index, row in enumerate(data):
            reaction = REACTION_NAME.search(row['reaction']).group(1)

            if self.reactions[index].name == reaction:
                self.reactions[index].set_flux(flux_type, row['first_flux'],
                                               row['second_flux'])
            else:
                loggers.aam_logger.warning(
                    'FluxError: Reaction name does not match reaction at index.',
                    extra={
                        'reaction': self.reactions,
                        'reaction_index': index,
                        'reaction_name': reaction
                    })

    def init_first_row(self, first_header: str, second_header: str):
        first_header, second_header = first_header.strip().upper(
        ), second_header.strip().upper()

        is_error, errors = flux_upload.validate_flux(first_header,
                                                     second_header)

        if is_error and errors is not None:
            raise handler.InvalidUsage(status_code=400, payload=errors)

        self.flux_model = True

        return '_'.join([first_header, second_header])

    def init_row(self, name: str, identifier: str, index: int,
                 row: dict[Any, Any], flux_type: Optional[str]):
        reaction = Reaction(name, identifier, index)
        reaction.arrow = row['arrow']
        reaction.set_identifier(identifier)
        reaction.reversible = row['arrow'] in REVERSIBLE

        if flux_type is not None:
            reaction.set_flux(flux_type, row['first_flux'], row['second_flux'])
        else:
            if row['first_flux'] or row['second_flux']:
                raise NoFluxTypeError()

        if row['arrow'] in REVERSIBLE or row['arrow'] in PRODUCTS_RIGHT:
            substrates = row['substrates']
            products = row['products']
        else:
            products = row['substrates']
            substrates = row['products']

        if reaction.identifier is None:
            metabolites = reaction.set_metabolites(substrates, products)
            reaction.set_atom_mapping(metabolites)
            if reaction.mappings:
                for compound in reaction.mappings[0]:
                    if compound['metabolite'] not in self.metabolites:
                        met = Metabolite(compound['name'],
                                         compound['metabolite'])
                        self.metabolites.setdefault(compound['metabolite'],
                                                    met)
                    else:
                        met = self.metabolites.get(compound['metabolite'])

                    if met is not None:
                        reaction.add_compound(met, compound['reactant'])
                        self.metabolites.get(
                            compound['metabolite']).add_reaction(
                                reaction, compound['reactant'])
        else:
            database_reaction: CasmReaction = casm.Reaction.query.get(
                reaction.identifier)
            metabolites = reaction.set_metabolites(substrates, products)

            try:
                compounds_base = database_reaction.compounds
            except AttributeError:

                loggers.aam_logger.error(
                    'NoCompoundsError: No database compounds for the reaction',
                    extra={'reaction': reaction.__dict__})
            else:

                compounds = {
                    compound.compound_id: compound.compound
                    for compound in compounds_base
                }

                for reactant in ['substrate', 'product']:
                    if not metabolites['substrate'] and not metabolites[
                            'product']:
                        for compound in compounds_base:
                            if compound.compound_id in self.metabolites:
                                met = self.metabolites.get(
                                    compound.compound_id)
                                metabolite_name = met.name
                            else:
                                metabolite_name = compound.compound.name
                            metabolites[compound.reactant].append({
                                'identifier':
                                compound.compound_id,
                                'name':
                                metabolite_name,
                                'const':
                                compound.quantity,
                                'mapping':
                                None
                            })
                    metabos: "List[MetaboliteTyping]" = metabolites[reactant]

                    for metabo in metabos:
                        metabo_identifier = metabo['identifier']
                        if metabo_identifier is not None and metabo_identifier in compounds:
                            compound = compounds[metabo_identifier]
                            if compound.id not in self.metabolites:

                                met = Metabolite(metabo['name'],
                                                 metabo_identifier,
                                                 qty=metabo['const'])
                                self.metabolites.setdefault(
                                    metabo_identifier, met)
                            else:
                                met = self.metabolites.get(metabo_identifier)

                            if met is not None:
                                reaction.add_compound(met, reactant)
                                # self.metabolites.get(
                                #     metabo_identifier).add_reaction(
                                #         reaction, reactant)
                            else:
                                # TODO: Error message
                                print('ERROR MET')
                        #TODO: Error message
                        # else:
                        #     print('ERROR', reaction, metabo, compounds)

            reaction.set_atom_mapping(metabolites)
        self.reactions.append(reaction)

    def initialize_from_identifiers(self, reactions):
        for index, entry in enumerate(reactions):
            reaction = CasmReaction.query.get(entry['reaction']['id'])

    def initialize_reactions(self, file: str):
        self.reactions = []
        self.file = csv.DictReader(file.splitlines(),
                                   fieldnames=('reaction', 'substrates',
                                               'arrow', 'products',
                                               'first_flux', 'second_flux'))

        flux_type = None
        index_add_on = 0
        for index, row in enumerate(self.file):
            if index == 0:
                if row['first_flux'] is not None and row[
                        'second_flux'] is not None and (
                            row['first_flux'].upper() == 'FORWARD'
                            or row['first_flux'].upper() == 'NET'):
                    flux_type = self.init_first_row(row['first_flux'],
                                                    row['second_flux'])
                elif row['reaction'].upper() in [
                        'NAME', 'REACTION', 'REACTION_NAME'
                ]:
                    if row['first_flux']:
                        raise FluxModelIdentificationError(
                            row['first_flux'], row['second_flux'])
                    else:
                        continue

                else:
                    index_add_on = 1
                    match = VALID_REACTION_IDENTIFIER.search(row['reaction'])
                    if match is not None:
                        name, identifier = match.groups()

                        if identifier is None:
                            identifier = name
                        self.init_row(name, identifier, index + index_add_on,
                                      row, flux_type)
            else:
                match = VALID_REACTION_IDENTIFIER.search(row['reaction'])
                if match is not None:
                    name, identifier = match.groups()

                    if identifier is None:
                        identifier = name
                    self.init_row(name, identifier, index + index_add_on, row,
                                  flux_type)

        if AtomMapping.reaction_errors:
            print(AtomMapping.reaction_errors)
            raise MissingAtomMappingError(AtomMapping.reaction_errors)

        # self.elements = {}
        # for compound in self.metabolites.values():
        #     for element in compound.elements:
        #         if element['symbol'] not in self.elements:
        #             self.elements.setdefault(
        #                 element['symbol'],
        #                 ele.Element(element['identifier'], element['name'],
        #                             element['symbol']))

        #         self.elements.get(element['symbol']).add_compound(compound)

        # if not self.elements:
        #     self.elements.setdefault('C', ele.Element(None, 'Carbon', 'C'))
        #     for compound in self.metabolites.values():
        #         self.elements.get('C').add_compound(compound)

    def load(self, reactions):
        self.reactions = []
        self.metabolites = {}

        for reaction in reactions:
            reaction_obj = Reaction(reaction['name'],
                                    reaction['database_identifier'],
                                    reaction['index'])
            reaction_obj.set_identifier(reaction['identifier'])
            reaction_obj.mappings = reaction['mappings']
            reaction_obj.forward = reaction['forward']
            reaction_obj.reverse = reaction['reverse']
            reaction_obj.reversible = reaction['reversible']
            reaction_obj.arrow = reaction['arrow']
            reaction_obj.curated = reaction['curated']

            for reactant in ['substrate', 'product']:
                compounds = reaction['metabolites'][reactant]
                for compound in compounds:
                    if compound['identifier'] not in self.metabolites:

                        met = Metabolite(compound['name'],
                                         compound['identifier'],
                                         compound['elements'], compound['qty'])

                        self.metabolites.setdefault(compound['identifier'],
                                                    met)
                    else:
                        met = self.metabolites.get(compound['identifier'])

                    if met is not None:
                        reaction_obj.add_compound(met, reactant)
                        self.metabolites.get(
                            compound['identifier']).add_reaction(
                                reaction_obj, reactant)
                    else:
                        # TODO: Error Message
                        print('ERROR MET')

            self.reactions.append(reaction_obj)


class Reaction:
    """Get casm reaction based on provided identifier.
    """
    def __init__(self, name: str, database_identifier: str, index: int):
        self.name = name
        self.database_identifier = database_identifier
        self.index = index
        self.forward = None
        self.reverse = None
        self.arrow = None
        self.reversible = False
        self.user_mapping = False
        self.identifier = None

        self.metabolites = {'substrate': [], 'product': []}
        self.mappings = []
        self.conversion = {}

    def set_identifier(self, identifier: Union[str, int]) -> Optional[int]:
        if isinstance(identifier, str):
            reaction_source = casm.ReactionSource.query.filter(
                casm.ReactionSource.database_identifier == identifier).first()
            try:
                id: int = reaction_source.reaction.id
                self.identifier = id
            except AttributeError:
                self.identifier = None
        else:
            self.identifier = identifier

    def add_compound(self, compound: Metabolite, reactant: str):
        if compound not in self.metabolites.get(reactant):
            self.metabolites.get(reactant).append(compound)

    def set_metabolites(self, substrates: str,
                        products: str) -> "MetabolitesTyping":
        metabolites: "MetabolitesTyping" = {'substrate': [], 'product': []}
        reactants = ['substrate', 'product']

        for index, reactant in enumerate([substrates, products]):
            if reactant is None:
                continue
            for element in reactant.split(' + '):
                result = VALID_REACTION_IDENTIFIER_NEW.search(element)
                if result is not None:
                    result = result.groupdict()
                    result = {k: v for k, v in result.items() if v is not None}

                    name = result['name']
                    try:
                        const = int(result['const'])
                    except KeyError:
                        const = 1

                    identifier, mapping, compound_id = None, None, None
                    for key, value in result.items():
                        if 'id' in key:
                            identifier = value
                        elif 'aam' in key:
                            mapping = value

                    if mapping:
                        self.user_mapping = True
                    if identifier is not None and identifier not in METABOLITES:
                        compound: Optional[
                            casm.
                            CompoundSource] = casm.CompoundSource.query.filter(
                                casm.CompoundSource.database_identifier ==
                                identifier).first()
                        if compound is not None:
                            compound_id: Optional[int] = compound.compound_id
                        else:
                            if 'CASM' in identifier:
                                identifier = identifier.split('_')[1]
                                compound = casm.Compound.query.get(identifier)
                                if compound is not None:
                                    compound_id = compound.id

                        METABOLITES.setdefault(identifier, compound_id)
                    elif identifier is not None:
                        compound_id = METABOLITES.get(identifier)

                    metabolite: "MetaboliteTyping" = {
                        'const': const,
                        'name': name,
                        'identifier': compound_id,
                        'mapping': mapping
                    }
                    metabolites[reactants[index]].append(metabolite)
        return metabolites

    def set_atom_mapping(self, metabolites: "MetabolitesTyping"):
        atom_mapping = AtomMapping(self.name)

        print(self.identifier, self.user_mapping)
        if self.identifier is None or self.user_mapping:
            self.curated = 'user'
            atom_mapping.set_user(metabolites)

        else:
            reaction: Optional[casm.Reaction] = casm.Reaction.query.get(
                self.identifier)

            if reaction is not None:
                self.curated = reaction.updated
                atom_transition = reaction.json
                symmetry = reaction.symmetry

                if atom_transition and symmetry:
                    atom_mapping.set_symmetry(metabolites, atom_transition)

                elif atom_transition:
                    atom_mapping.set_database(metabolites, atom_transition)

        self.mappings = atom_mapping.mappings
        self.conversion = atom_mapping.conversion
        if not self.mappings:
            logging_reaction = {
                'name': self.name,
                'database_identifier': self.database_identifier,
                'identifier': self.identifier,
                'user_mapping': self.user_mapping,
                'reversible': self.reversible,
                'curated': self.curated,
                'metabolites': self.metabolites,
                'mappings': self.mappings
            }
            loggers.aam_logger.warning(
                'No atom mapping was found for the reaction!',
                extra={'reaction': logging_reaction})

    def set_flux(self, flux_type: str, first: str, second: str):
        """Identify and set fluxes.

        Args:
            flux_type (str): Type of flux.
            first_flux (str): First flux.
            second_flux (str): Second flux.
        """
        try:
            first_flux = float(first)
        except ValueError:
            first_flux = 0
        try:
            second_flux = float(second)
        except ValueError:
            second_flux = 0

        if flux_type == 'NET_EXCHANGE':
            self.forward, self.reverse = set_net_exchange(
                first_flux, second_flux)

        elif flux_type == 'FORWARD_REVERSE':
            self.forward, self.reverse = (first_flux, second_flux)

    def __repr__(self):
        return '<{0} {1!r}>'.format(
            self.__class__.__name__,
            (self.identifier, self.name, self.database_identifier, self.index))


def set_net_exchange(first_flux: float,
                     second_flux: float) -> Tuple[float, float]:
    """Setting of net_exchange flux based on first flux.

    Args:
        first_flux (str): The first flux.
        second_flux (str): The second flux.
    """
    if float(first_flux) >= 0:
        forward_flux = float(first_flux) + float(second_flux)
        reverse_flux = float(second_flux)

    else:
        forward_flux = float(second_flux)
        reverse_flux = -(float(first_flux) - float(second_flux))

    return forward_flux, reverse_flux


class AtomMapping:
    reaction_errors = []

    def __init__(self, reaction: str, element: str = 'C'):
        self.abc_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.conversion = {}
        self.counter = 0

        self.mappings = []
        self.reaction = reaction
        self.element = element

    def set_symmetry(self, metabolites: "MetabolitesTyping",
                     atom_transition: "AtomTransitionTyping"):
        groups = []
        for mol_file in atom_transition['mol_files']:
            for atom in mol_file['atom_block']:
                if atom['symbol'] == self.element:
                    if '.' in str(atom['aam']):
                        aam = str(atom['aam'])
                        group, number = aam.split('.')
                        if group not in groups:
                            groups.append(group)

        if groups:
            for index in range(2**len(groups)):
                mapping = []
                for reactant in ['substrate', 'product']:
                    compounds = metabolites[reactant]
                    for compound in compounds:
                        for mol_file in atom_transition['mol_files']:
                            if mol_file['id'] == compound['identifier']:
                                abc_string = self.set_symmetry_string(
                                    mol_file['atom_block'], reactant, index)
                                compound_mapping = self.set_compound_mapping(
                                    compound['name'], compound['identifier'],
                                    reactant, abc_string, compound['const'])
                                mapping.append(compound_mapping)

                self.mappings.append(mapping)
        else:
            self.set_database(metabolites, atom_transition)

    def set_symmetry_string(self, atom_block: "List[AtomBlockTyping]",
                            reactant: str, index: int) -> str:
        number_order = {}
        abc_string = ''
        for atom in atom_block:
            if atom['symbol'] == self.element:
                if '.' in str(atom['aam']):
                    self.conversion.setdefault(atom['aam'], [])
                    if len(self.conversion[atom['aam']]) < 2:
                        self.conversion[atom['aam']].append(self.counter)
                        self.counter += 1
                elif atom['aam'] not in self.conversion:
                    self.conversion.setdefault(atom['aam'], self.counter)
                    self.counter += 1

                conversion = self.conversion[atom['aam']]
                if isinstance(self.conversion[atom['aam']], list):
                    number_order.setdefault(atom['aam'], 0)
                    if reactant == 'product':
                        conversion = self.conversion[atom['aam']][
                            -number_order[atom['aam']] - index]
                    else:
                        conversion = self.conversion[atom['aam']][number_order[
                            atom['aam']]]
                    number_order[atom['aam']] += 1
                abc_string += self.abc_string[conversion]
        return abc_string

    def set_database(self, metabolites: "MetabolitesTyping",
                     atom_transition: "AtomTransitionTyping"):
        mapping = []
        for reactant in ['substrate', 'product']:
            compounds = metabolites[reactant]
            for compound in compounds:
                for mol_file in atom_transition['mol_files']:
                    if mol_file['id'] == compound['identifier']:
                        try:
                            abc_string = self.set(mol_file['atom_block'])
                        except IndexError as error:
                            self.set_over_limit(metabolites, atom_transition)
                            break
                        compound_mapping = self.set_compound_mapping(
                            compound['name'], compound['identifier'], reactant,
                            abc_string, compound['const'])
                        mapping.append(compound_mapping)
        self.mappings.append(mapping)

    def set_user(self, metabolites: "MetabolitesTyping"):
        print(metabolites)
        mapping = []
        for reactant in ['substrate', 'product']:
            compounds = metabolites[reactant]
            for compound in compounds:
                if compound['identifier'] is None:
                    compound['identifier'] = compound['name']
                user_mapping = compound['mapping']
                if user_mapping is None:
                    continue
                    # AtomMapping.reaction_errors.append(self.reaction)
                    # break
                else:
                    compound_mapping = self.set_compound_mapping(
                        compound['name'], compound['identifier'], reactant,
                        user_mapping, compound['const'])
                    mapping.append(compound_mapping)

        self.mappings.append(mapping)

    def set_compound_mapping(self, name: str, metabolite: Optional[Union[int,
                                                                         str]],
                             reactant: str, mapping: str,
                             const: float) -> "MappingTyping":
        return {
            'name': name,
            'metabolite': metabolite,
            'reactant': reactant,
            'mapping': mapping,
            'const': const
        }

    def set(self,
            atom_block: "List[AtomBlockTyping]",
            element: str = 'C') -> str:
        abc_string = ''
        for atom in atom_block:
            if atom['symbol'] == element:
                if atom['aam'] not in self.conversion:
                    self.conversion.setdefault(atom['aam'], self.counter)
                    self.counter += 1

                abc_string += self.abc_string[self.conversion[atom['aam']]]

        return abc_string

    def set_over_limit(self,
                       metabolites: "MetabolitesTyping",
                       atom_transition: "AtomTransitionTyping",
                       element: str = 'C'):
        mapping = []
        for reactant in ['substrate', 'product']:
            compounds = metabolites[reactant]
            for compound in compounds:
                for mol_file in atom_transition['mol_files']:
                    if mol_file['id'] == compound['identifier']:
                        abc_string = ''
                        for atom in mol_file['atom_block']:
                            if atom['symbol'] == element:
                                if atom['aam'] not in self.conversion:
                                    self.conversion.setdefault(
                                        atom['aam'], self.counter)
                                    self.counter += 1

                                if abc_string == '':
                                    abc_string += f'{self.conversion[atom["aam"]]}'
                                else:
                                    abc_string += f'.{self.conversion[atom["aam"]]}'

                        compound_mapping = self.set_compound_mapping(
                            compound['name'], compound['identifier'], reactant,
                            abc_string, compound['const'])
                        mapping.append(compound_mapping)
        self.mappings.append(mapping)

    def __repr__(self):
        return '<{0} {1!r}>'.format(self.__class__.__name__, (self.mappings))
