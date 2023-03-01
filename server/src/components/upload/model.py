from __future__ import annotations

import csv
import re
from typing import Dict, Iterator, List, Optional, TextIO, Tuple

from src.components.upload.components import Metabolite, Reaction

VALID_REACTION_IDENTIFIER = re.compile(
    r'''
    (?P<const>\d+(?:\.\d+)?\s)?(?P<name>[^\s\+]\S*)(?:\s\((?P<aam>[\S]*)\)\s*|\s\[(?P<id>[\S]*)\]\s*)?(?:\s*\((?P<aam2>[\S]*)\)\s*|\s*\[(?P<id2>[\S]*)\]\s*)?
    ''', re.VERBOSE)

CASM_ID_IDENTIFIER = re.compile(r'\[CASM_(\d*?)\]', re.VERBOSE)


class AtomMappingModel():
    def __init__(self, verbose: bool = False):
        self.reactions: Dict[str, Reaction] = {}
        self.metabolites: Dict[str, Metabolite] = {}
        self.to_add = []

        self._verbose = verbose

    def _add_flux(self, row: List[str], index: int) -> None:
        reaction = self.reactions.get(row[0])
        if reaction is None:
            self.to_add.append(row[0])
            raise NameError(f'Reaction {row[0]} not in AtomMappingModel')

        reaction.set_flux(self.flux_type, row[1], row[2])

    def decode_flux(self, model: Iterator[List[str]],
                    flux_type: str) -> AtomMappingModel:
        self.flux_type = flux_type
        for model_index, row in enumerate(model):
            try:
                self._add_flux(row, model_index)
            except NameError as e:
                if self._verbose:
                    print(e)

        return self

    def _decode_metamdb(self, model: List[dict]) -> AtomMappingModel:
        for user_reaction in model:
            reaction_name = user_reaction['name']

            reaction = Reaction(reaction_name, user_reaction['arrow'],
                                user_reaction['index'])

            try:
                self._set_metamdb_metabolites(user_reaction['mappings'][0],
                                              reaction)
            except NameError as e:
                if self._verbose:
                    print(e)
            except IndexError as e:
                if self._verbose:
                    print(e)
            else:
                self.reactions.setdefault(reaction_name, reaction)

        return self

    def decode(self, model: Iterator[List[str]]) -> AtomMappingModel:
        for model_index, row in enumerate(model):
            self._create_reaction(row, model_index)

        return self

    def _create_reaction(self, row: List[str], index: int) -> None:
        reaction = Reaction(row[0], row[2], index)

        try:
            self._set_metabolites(row[1], row[3], reaction)
        except NameError as e:
            if self._verbose:
                print(e)
        else:
            self.reactions.setdefault(row[0], reaction)

    def _identifiy_compoung_string(
            self, compound: str) -> Tuple[Optional[str], Optional[str]]:
        result = VALID_REACTION_IDENTIFIER.search(compound)
        if result is not None:
            result = result.groupdict()
            result = {k: str(v) for k, v in result.items() if v is not None}

            name, mapping = None, None
            for key, value in result.items():
                if 'aam' in key:
                    mapping = value
                elif 'name' == key:
                    name = value
            return name, mapping
        return None, None

    def _set_metamdb_metabolites(self, compounds: List[dict],
                                 reaction: Reaction):
        metabolites: Dict[str, List[Tuple[Metabolite, str | None]]] = {
            'substrate': [],
            'product': []
        }

        for compound in compounds:
            name, mapping, reactant = compound['name'], compound[
                'mapping'], compound['reactant']

            if name is None:
                raise NameError(
                    f'Reaction {reaction.name} contains a reactant without a name!'
                )

            try:
                metabolite = self.metabolites[name]
            except KeyError:
                if mapping is None:
                    atom_count = None
                elif '.' in mapping:
                    atom_count = len(mapping.split('.'))
                else:
                    atom_count = len(mapping)

                metabolite = Metabolite(name, atom_count)
                self.metabolites.setdefault(name, metabolite)

            metabolites[reactant].append((metabolite, mapping))

        for reactant, elements in metabolites.items():
            for metabolite in elements:
                metabolite[0].add_reaction(
                    reaction, metabolite, reactant,
                    metabolites['substrate' if reactant ==
                                'product' else 'product'])

    def _set_metabolites(self, substrates: str, products: str,
                         reaction: Reaction):
        metabolites: Dict[str, List[Tuple[Metabolite, str | None]]] = {
            'substrate': [],
            'product': []
        }
        reactants = ['substrate', 'product']
        if reaction.products_right:
            substrates_products = [substrates, products]
        else:
            substrates_products = [products, substrates]
        for index, reactant in enumerate(substrates_products):
            if reactant is None:
                continue

            for element in reactant.split(' + '):
                name, mapping = self._identifiy_compoung_string(element)

                if name is None:
                    raise NameError(
                        f'Reaction {reaction.name} contains a {reactants[index]} without a name!'
                    )

                try:
                    metabolite = self.metabolites[name]
                except KeyError:
                    if mapping is None:
                        atom_count = None
                    elif '.' in mapping:
                        atom_count = len(mapping.split('.'))
                    else:
                        atom_count = len(mapping)

                    metabolite = Metabolite(name, atom_count)
                    self.metabolites.setdefault(name, metabolite)

                metabolites[reactants[index]].append((metabolite, mapping))

        for reactant, elements in metabolites.items():
            for metabolite in elements:
                metabolite[0].add_reaction(
                    reaction, metabolite, reactant,
                    metabolites['substrate' if reactant ==
                                'product' else 'product'])


def read_csv_mapping_model(fp: TextIO) -> AtomMappingModel:
    return read_mapping_model(list(csv.reader(fp)))


def read_mapping_model(model: List[List[str]]) -> AtomMappingModel:
    required_cols = ('name', 'substrates', 'arrow', 'products')
    model_iter = iter(model)
    head = next(model_iter)

    missing_required = [
        index for index in range(len(required_cols))
        if required_cols[index] != head[index].lower()
    ]
    if len(missing_required) > 0:
        raise Exception(
            f'The columns {required_cols} are required in the specified order!'
        )
    return AtomMappingModel().decode(model_iter)


def read_csv_flux_model(fp: TextIO,
                        mapping_model: AtomMappingModel) -> AtomMappingModel:
    return read_flux_model(list(csv.reader(fp)), mapping_model)


def read_flux_model(model: List[List[str]],
                    mapping_model: AtomMappingModel) -> AtomMappingModel:
    required_cols_net = ('name', 'net', 'exchange')
    required_cols_forward = ('name', 'forward', 'reverse')
    model_iter = iter(model)
    head = next(model_iter)

    missing_required_net = [
        index for index in range(len(required_cols_net))
        if required_cols_net[index] != head[index].lower()
    ]

    missing_required_forward = [
        index for index in range(len(required_cols_forward))
        if required_cols_forward[index] != head[index].lower()
    ]
    if len(missing_required_net) > 0 and len(missing_required_forward) > 0:
        raise Exception(
            f'The columns {required_cols_net}/{required_cols_forward} are required in the specified order!'
        )
    flux_type = f'{head[1].upper()}_{head[2].upper()}'
    return mapping_model.decode_flux(model_iter, flux_type)
