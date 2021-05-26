from __future__ import annotations

import itertools
from re import sub
from typing import TYPE_CHECKING, Any, List, Optional, Union

import numpy as np
from numpy.lib.utils import source
from numpy.linalg.linalg import norm
from src.errors.handler import InvalidUsage

if TYPE_CHECKING:
    from src.components.upload.reaction import Reaction, ReactionModel
    from typings.casm.calculation import TracerTyping
    from typings.casm.reaction import MetaboliteElementsTyping


def generate_atoms(start: int, stop: int) -> List[int]:
    return [atom for atom in range(start, stop + 1)]


class EMU():
    def __init__(self, metabolite: str, identifier: Union[str, int],
                 atoms: List[int]):
        self.metabolite = metabolite
        self.identifier = identifier
        self.atoms = atoms

        self.sources = {}
        self.mid: List[float] = np.zeros(len(self.atoms) + 1)  # type: ignore
        self.name = '%s_%s' % (self.metabolite, ''.join(
            str(atom) for atom in self.atoms))

    def __len__(self):
        return len(self.atoms)

    def __getitem__(self, position):
        return self.atoms[position]

    def __repr__(self):
        return '<EMU object "%s">' % self.name

    def __str__(self):
        return self.name


class Metabolite():
    def __init__(self,
                 name: str,
                 identifier: int,
                 elements: "List[MetaboliteElementsTyping]" = None,
                 qty: int = 1):
        self.name = name
        self.identifier = identifier

        self.elements = []
        if elements is not None:
            self.elements = elements

        self.qty = qty

        self.reactions: dict[str, List[Reaction]] = {
            'producing': [],
            'dismanteling': []
        }
        self.emus: List[EMU] = []
        self.mapping = {}

    def get_atom_count(self, element: str) -> int:
        atom_count = 0

        for entry in self.elements:
            if entry['symbol'] == element:
                try:
                    atom_count = int(entry['qty'])
                # TODO: handle error
                except ValueError:
                    print('ATOM COUNT ERROR')

        return atom_count

    def add_reaction(self, reaction: Reaction, reactant: str):
        if (reactant == 'product' or reaction.reversible
            ) and reaction not in self.reactions['producing']:
            self.reactions['producing'].append(reaction)

        elif reactant == 'substrate' and reaction not in self.reactions[
                'dismanteling']:
            self.reactions['dismanteling'].append(reaction)

    def __repr__(self):
        return '<{0} {1!r}>'.format(self.__class__.__name__,
                                    (self.name, self.identifier))

    def get_emu(self, atoms: List[int]) -> EMU:
        emu = self._search_emus(atoms)

        if not emu:
            emu = EMU(self.name, self.identifier, atoms)
            self.emus.append(emu)

        return emu

    def _search_emus(self, atoms: List[int]) -> Optional[EMU]:
        for emu in self.emus:
            if emu.atoms == atoms:
                return emu

    def get_mapping(self):
        if self.mapping:
            return self.mapping

        for reaction in self.reactions['producing']:
            for mapping_index, mapping_obj in enumerate(reaction.mappings):
                reactant, mapping = None, None
                for mapping_dict in mapping_obj:
                    if mapping_dict['metabolite'] == self.identifier:
                        if '.' in mapping_dict['mapping']:
                            mapping = mapping_dict['mapping'].split('.')
                        else:
                            mapping = mapping_dict['mapping']
                        reactant = mapping_dict['reactant']
                        break

                # TODO: error message
                if reactant is None:
                    print('REACTANT IS NONE')
                    continue
                elif mapping is None:
                    print('MAPPING IS NONE')
                    continue
                else:
                    substrates = {}
                    for index, mapping_dict in enumerate(mapping_obj):
                        if '.' in mapping_dict['mapping']:
                            mapping_new = mapping_dict['mapping'].split('.')
                        else:
                            mapping_new = mapping_dict['mapping']
                        if reactant != mapping_dict['reactant'] and any(
                                aam_letter in mapping
                                for aam_letter in mapping_new):
                            substrates.setdefault(
                                index, {
                                    'index': [
                                        aam_letter
                                        for aam_letter in mapping_new
                                        if aam_letter in mapping
                                    ]
                                })
                    for index in substrates:
                        substrate_mapping = reaction.mappings[mapping_index][
                            index]['mapping']
                        if '.' in substrate_mapping:
                            substrate_mapping = substrate_mapping.split('.')

                        substrates[index]['source'] = [
                            substrate_mapping.index(atom) + 1
                            for atom in substrates[index]['index']
                        ]
                        substrates[index]['index'] = [
                            mapping.index(atom) + 1
                            for atom in substrates[index]['index']
                        ]

                        substrates[index]['index'], substrates[index][
                            'source'] = (list(x) for x in zip(*sorted(
                                zip(substrates[index]['index'],
                                    substrates[index]['source']))))

                        substrates[index]['name'] = reaction.mappings[
                            mapping_index][index]['metabolite']

                    if self in reaction.metabolites['product']:
                        direction = 'forward'
                        flux = reaction.forward

                    else:
                        direction = 'reverse'
                        flux = reaction.reverse

                    flux = flux / len(reaction.mappings)

                    self.mapping.setdefault(
                        '%s_%s_%s' %
                        (reaction.name, f'AAM{mapping_index}', direction),
                        [{
                            'name': mappings['name'],
                            'source': mappings['source'],
                            'index': mappings['index'],
                            'flux': flux
                        } for mappings in substrates.values()])

        return self.mapping


class Model():
    def __init__(self, model: ReactionModel, tracer: "TracerTyping",
                 products: List[str], element):
        self.model = model
        # tracer = {'metabolite': '54128', 'labeling': '111111', 'purity': '0.5'}
        # products = [
        #     '24883', '4153', '27250', '48690', '55714', '27244', '4060',
        #     '69702', '91446', '22155', '11281', '11397', '4153', '34530',
        #     '4150'
        # ]
        self.substrates = self._initialize_substrates(tracer)
        self.targets = self._initialize_targets(products)

        self.models = {}
        self.saved_emus: List[EMU] = []
        self.processed_emus: List[EMU] = []
        self.substrate_emus: List[EMU] = []

        self._initialize_target_emus()
        self._decompose_emus()
        self._initialize_substrate_emus()

    def _initialize_substrates(
            self,
            tracer: "TracerTyping") -> dict[Union[str, int], dict[str, str]]:
        try:
            metabolite = str(tracer['metabolite'])
        #TODO: Error message
        except ValueError:
            metabolite = tracer['metabolite']

        substrates = {
            metabolite: {
                'labeling': tracer['labeling'],
                'purity': tracer['purity']
            }
        }

        extern_ending = ['.ext', '.snk', '64158']
        # extern_ending = ['_ex', '_ex_b', '64158']
        # extern_ending = []

        for metabolite in self.model.metabolites.values():
            for ending in extern_ending:
                if (ending in metabolite.name
                        and metabolite.name not in substrates.keys()) or (
                            ending == metabolite.identifier
                            and metabolite.name not in substrates.keys()):
                    substrates.setdefault(metabolite.identifier, {
                        'labeling': '0' * metabolite.qty,
                        'purity': '1'
                    })
        return substrates

    def _initialize_targets(self, targets: List[str]) -> List[Metabolite]:
        new_targets = []
        if targets:
            for target in targets:
                new_target = str(target)
                new_targets.append(self.model.metabolites[new_target])
        else:
            for metabolite in self.model.metabolites.values():
                if metabolite.identifier not in self.substrates.keys():
                    new_target = str(metabolite.identifier)

                    new_targets.append(self.model.metabolites[new_target])

        return new_targets

    def _initialize_target_emus(self):
        for metabolite in self.targets:
            atom_count = metabolite.get_atom_count('C')
            atoms = generate_atoms(1, atom_count)
            emu = metabolite.get_emu(atoms)

            self._save_emu(emu)

    def _decompose_emus(self):
        self.saved_emus.sort(key=len, reverse=True)
        new_emu = False
        while self.saved_emus or new_emu:
            if new_emu:
                emu = new_emu

            else:
                emu = self.saved_emus.pop(
                    self.saved_emus.index(max(self.saved_emus, key=len)))

            new_emu = False
            metabolite = self.model.metabolites[emu.identifier]

            metabolite_mapping = metabolite.get_mapping()

            for index, (reaction,
                        mapping) in enumerate(metabolite_mapping.items()):

                for metabolite_map in mapping:
                    producing_metabolite = self.model.metabolites[
                        metabolite_map['name']]

                    source_atoms = [
                        source for source, index in zip(
                            metabolite_map['source'], metabolite_map['index'])
                        if index in emu
                    ]

                    if not source_atoms:
                        continue
                    if metabolite_map['flux'] == 0:
                        continue

                    source_emu = producing_metabolite.get_emu(source_atoms)

                    emu.sources.setdefault(reaction, {})
                    emu.sources[reaction].setdefault('emus',
                                                     []).append(source_emu)
                    emu.sources[reaction].setdefault('flux',
                                                     metabolite_map['flux'])

                    if producing_metabolite.identifier not in self.substrates and source_emu not in self.processed_emus:
                        if len(source_emu) != len(emu) or new_emu:
                            self._save_emu(source_emu)

                        else:
                            new_emu = source_emu

            self._remove_emu(emu)

    def _save_emu(self, emu):
        if emu not in self.saved_emus and emu not in self.processed_emus:
            self.saved_emus.append(emu)

    def _remove_emu(self, emu):
        if emu in self.saved_emus:
            self.saved_emus.remove(emu)

        if emu not in self.processed_emus:
            self.processed_emus.append(emu)

    # TODO: Optimize Initialisation
    def _initialize_substrate_emus(self):
        for substrate, params in self.substrates.items():
            labeling = params['labeling']
            purity = float(params['purity'])
            impurity = 1 - purity

            metabolite = self.model.metabolites[str(substrate)]
            for emu in metabolite.emus:
                emu_labeling = [
                    int(labeling[index]) for index in range(len(labeling))
                    if index + 1 in emu.atoms
                ]

                mass_increase = sum(emu_labeling)

                if mass_increase:
                    for mass in range(mass_increase + 1):
                        if mass == mass_increase:
                            emu.mid[mass] = purity * 1.0
                        elif mass == 0:
                            emu.mid[mass] = impurity * 1.0
                        else:
                            emu.mid[mass] = 0.0

                else:
                    emu.mid[0] = 1.0

                self.substrate_emus.append(emu)

    def _generate_labeling_combinations(self, labels, mass):
        combinations = list(
            itertools.chain.from_iterable(
                itertools.combinations(labels, count)
                for count in range(len(labels) + 1)))
        return [
            combination for combination in combinations
            if sum(combination) == mass
        ]

    def calculate_mids(self):
        for emu_size in range(len(min(self.processed_emus, key=len)),
                              len(max(self.processed_emus, key=len)) + 1):
            if emu_size == 0:
                continue
            emu_network = [
                emu for emu in self.processed_emus
                if len(emu) == emu_size and emu.sources
            ]
            if emu_network:
                seen_emus = []
                adj_matrix = np.zeros(  # type: ignore
                    [len(emu_network), len(emu_network)])
                sub_matrix = np.empty(  # type: ignore
                    (len(emu_network), 0), int)

                for emu_index in range(len(emu_network)):
                    for reaction, source_emus in emu_network[
                            emu_index].sources.items():

                        if any(source_emu not in self.substrate_emus
                               for source_emu in source_emus['emus']):
                            try:

                                adj_matrix[emu_index][emu_network.index(
                                    source_emus['emus']
                                    [0])] += source_emus['flux'] / 1
                            # TODO: Error message
                            except ValueError as error_message:
                                print(error_message)

                        else:
                            if source_emus['emus'] not in seen_emus:
                                seen_emus.append(source_emus['emus'])
                                sub_matrix = np.append(
                                    sub_matrix,
                                    np.zeros([  # type: ignore
                                        len(emu_network), 1
                                    ]),
                                    axis=1)

                            sub_matrix[emu_index][seen_emus.index(
                                source_emus['emus']
                            )] -= source_emus['flux'] / 1

                        adj_matrix[emu_index][
                            emu_index] -= source_emus['flux'] * 1

                substrate_mids = self._calculate_substrate_mids(seen_emus)

                try:
                    target_mids = np.dot(  # type: ignore
                        np.dot(  # type: ignore 
                            np.linalg.inv(adj_matrix), sub_matrix),
                        substrate_mids)
                except np.linalg.LinAlgError:
                    zero_rows = np.where(~adj_matrix.any(  # type: ignore
                        axis=1))[0]
                    not_produced = set()
                    for row in zero_rows:
                        not_produced.add(emu_network[row].metabolite)
                    if not_produced:
                        error = {
                            'message':
                            "Not produced metabolites %s" %
                            ', '.join(list(not_produced))
                        }
                    else:
                        error = {
                            'message':
                            "Uploaded flux and reaction model cant be solved due to a 'singular matrix error'"
                        }
                    raise InvalidUsage(status_code=400, payload=error)

                for emu, mid in zip(emu_network, target_mids):
                    emu.mid = mid
                self.substrate_emus += emu_network

    def _calculate_substrate_mids(self, emus):
        mids = [self._get_mid(emu) for emu in emus]

        max_length = len(max(mids, key=len))

        adjusted_mids = [
            np.concatenate(  # type: ignore
                [mid, np.zeros(max_length - len(mid))])  # type: ignore
            for mid in mids
        ]

        return np.vstack(adjusted_mids)

    def _get_mid(self, mids):
        mid = mids[0].mid
        for index in range(1, len(mids)):
            mid = np.convolve(mid, mids[index].mid)
        return mid

    def get_mids(self) -> List[dict[str, Union[str, List[float]]]]:
        mids: List[dict[str, Union[str, List[float]]]] = []
        for target in self.targets:
            data = list(max(target.emus, key=len).mid)
            mid: dict[str, Union[str, List[float]]] = {
                'name': target.name,
                'data': data
            }
            mids.append(mid)

        return mids
