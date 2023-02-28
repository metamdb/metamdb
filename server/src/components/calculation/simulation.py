"""This module implements functionality for reaction models"""
from __future__ import annotations
import os
import multiprocessing
from typing import Dict, List

import numpy as np
from typing_extensions import TypedDict

from src.components.upload.components import EMU, Metabolite
from src.components.upload.model import AtomMappingModel

import logging
from logging.config import dictConfig

logging_config = {
    "version": 1,
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    },
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "ERROR"
        },
        "file": {
            "formatter": "std_out",
            "class": "logging.FileHandler",
            "level": "INFO",
            "filename": "all_messages.log"
        }
    },
    "formatters": {
        "std_out": {
            "format":
            "%(levelname)s : %(module)s : %(funcName)s : %(message)s",
        }
    },
}

dictConfig(logging_config)

logger = logging.getLogger()


class TracerTyping(TypedDict):
    name: str
    labeling: str
    purity: float | int
    enrichment: float | int


class SymmetryTyping(TypedDict):
    name: str
    symmetry: str


class Simulation():
    def __init__(self, model: AtomMappingModel):
        self.model = model

        self.emu_queue: List[EMU] = []
        self.generated_emus: Dict[int, Dict[EMU, int]] = {}
        self.substrate_emus: List[EMU] = []

        self.substrates: Dict[Metabolite, List[TracerTyping]] = {}
        self.targets: List[Metabolite] = []

        self.emu_reactions = {}

    def initialize_substrates(self,
                              tracers: List[TracerTyping],
                              as_substrate: List[str] = []):
        substrates: Dict[Metabolite, List[TracerTyping]] = {}

        for tracer in tracers:
            tracer_metabolite = self.model.metabolites.get(tracer['name'])
            if tracer_metabolite is None:
                print(
                    f'Tracer "{tracer["name"]}" is not in the Atom Mapping Model'
                )
                continue
            substrates.setdefault(tracer_metabolite, []).append(tracer)

        for substrate_name in as_substrate:
            substrate = self.model.metabolites.get(substrate_name)

            if substrate is None:
                print(
                    f'Tracer "{substrate_name}" is not in the Atom Mapping Model'
                )
                continue
            if substrate.atom_count is None:
                print(f'Tracer "{substrate_name}" has no Atom Mapping')
                continue

            new_substrate: TracerTyping = {
                'name': substrate_name,
                'labeling': substrate.atom_count * '0',
                'purity': 1,
                'enrichment': 1,
            }
            substrates.setdefault(substrate, []).append(new_substrate)

        for metabolite in self.model.metabolites.values():
            if not metabolite.prev and metabolite not in substrates:
                if metabolite.atom_count is None:
                    continue
                substrates.setdefault(metabolite, []).append({
                    'purity':
                    1,
                    'labeling':
                    metabolite.atom_count * '0',
                    'enrichment':
                    1,
                    'name':
                    metabolite.name
                })
        self.substrates = substrates

    def initialize_targets(self, targets: List[str] = []):
        new_targets = []
        if targets:
            for target_name in targets:
                target = self.model.metabolites.get(target_name)
                if target is None:
                    print(
                        f'Target "{target_name}" is not in the Atom Mapping Model'
                    )
                    continue
                if target.atom_count is None:
                    print(f'Target "{target.name}" has no Atom Mapping')
                    continue
                new_targets.append(target)

        else:
            for metabolite in self.model.metabolites.values():
                if self.substrates is None:
                    raise AttributeError(
                        'Call "initialize_substrates()" before initializing targets'
                    )
                if metabolite not in self.substrates and metabolite.atom_count and metabolite.atom_count is not None:
                    new_targets.append(metabolite)

        self.targets = new_targets

    def initialize_symmetries(self, symmetries: List[SymmetryTyping]):
        for symmetry in symmetries:
            if symmetry['name'] in self.model.metabolites:
                metabolite_produced = self.model.metabolites[
                    symmetry['name']].prev
                metabolite_next = self.model.metabolites[symmetry['name']].next

                new_mappings = []
                for source_metabolite, mappings in metabolite_produced.items():
                    while mappings:
                        mapping = mappings.pop()
                        other, old_source, direction, reaction, sym = mapping

                        new_mappings.append(
                            (symmetry['name'], source_metabolite,
                             (other, old_source, direction, reaction, True)))

                        if not sym:
                            source = ''.join(mapping[1][int(index) - 1]
                                             for index in symmetry['symmetry'])
                            new_mappings.append(
                                (symmetry['name'], source_metabolite,
                                 (other, source, direction, reaction, True)))

                for new_metabolite in metabolite_next.keys():
                    metabolite_produced = self.model.metabolites[
                        new_metabolite.name].prev
                    for source_metabolite, mappings in metabolite_produced.items(
                    ):
                        if source_metabolite.name == symmetry['name']:
                            while mappings:
                                mapping = mappings.pop()
                                other, old_source, direction, reaction, sym = mapping
                                new_mappings.append(
                                    (new_metabolite.name, source_metabolite,
                                     (other, old_source, direction, reaction,
                                      True)))

                                if not sym:
                                    source = ''.join(
                                        mapping[1][int(index) - 1]
                                        for index in symmetry['symmetry'])
                                    new_mappings.append(
                                        (new_metabolite.name,
                                         source_metabolite,
                                         (other, source, direction, reaction,
                                          True)))

                for mapping in new_mappings:
                    self.model.metabolites[mapping[0]].prev[mapping[1]].append(
                        mapping[2])

    def generate_emus(self):
        self._initialize_target_emus()
        self._decompose_emus()
        self._initialize_substrate_emus()

    def _decompose_emus(self):
        while self.emu_queue:
            emu = self.emu_queue.pop()

            metabolite = self.model.metabolites[emu.metabolite]

            for source_metabolite, mappings in metabolite.prev.items():
                for mapping in mappings:
                    other, source, direction, reaction, sym = mapping

                    flux = getattr(reaction, direction)
                    if flux is None or flux == 0.0:
                        continue

                    source_atoms: List[int] = []
                    for index, atom in enumerate(source, start=1):
                        if index in emu and atom in other:
                            source_atoms.append(other.index(atom) + 1)

                    if not source_atoms:
                        continue

                    source_atoms.sort()
                    emu_id = reaction.name
                    source_emu = source_metabolite.get_emu(source_atoms)
                    source_emu_len = len(source_emu)
                    self.generated_emus.setdefault(source_emu_len, {})

                    emu.sources.setdefault(emu_id, {})
                    emu.sources[emu_id].setdefault('flux', flux)
                    emu.sources[emu_id].setdefault('emus', [])
                    if source_emu not in emu.sources[emu_id]['emus']:
                        emu.sources[emu_id]['emus'].append(source_emu)
                    elif not sym:
                        emu.sources[emu_id]['emus'].append(source_emu)

                    if (emu, emu_id) not in source_emu.next:
                        source_emu.next.append((emu, emu_id))

                    self.emu_reactions.setdefault(reaction, None)
                    logger.warning('%s %s %s %s %s %s' %
                                   (emu.name, emu.atoms, reaction.name, flux,
                                    source_emu.name, source_emu.atoms))
                    if source_metabolite not in self.substrates and source_emu not in self.generated_emus[
                            source_emu_len]:

                        self.emu_queue.append(source_emu)
                        self.generated_emus.setdefault(
                            source_emu_len, {}).setdefault(
                                source_emu,
                                len(self.generated_emus[source_emu_len]))

    def reduce_emus(self):
        removed = {}
        for size, emus in self.generated_emus.items():
            for target, index in emus.items():
                if len(target.sources) == 1:
                    for sources in target.sources.values():
                        if not any(
                                len(source) != len(target)
                                for source in sources['emus']):
                            source = sources['emus'][0]

                            target.parent = source
                            removed.setdefault(size, []).append(target)

        for size, removed_emus in sorted(removed.items()):
            for removed_emu in removed_emus:
                for next_emu, reaction in removed_emu.next:
                    # print(removed_emu, next_emu, reaction, next_emu.sources)
                    if len(next_emu) not in removed or next_emu not in removed[
                            len(next_emu)]:
                        if next_emu != removed_emu.parent:
                            next_emu.sources[reaction]['emus'][
                                next_emu.sources[reaction]['emus'].index(
                                    removed_emu)] = removed_emu.parent
                        else:
                            next_emu.sources.pop(reaction)

                self.generated_emus[size].pop(removed_emu)

    def generate_emus_parallel(self, core_count: int):
        if isinstance(
                core_count, int
        ) and core_count >= 1 and core_count >= multiprocessing.cpu_count():
            self._initialize_target_emus()
            self._decompose_emus_parallel(core_count)
            self._initialize_substrate_emus()

    def _decompose_emus_parallel(self, core_count):
        self.emu_queue.sort(key=len, reverse=True)

        m = multiprocessing.Manager()
        worker_q = m.Queue()
        result_d = m.dict()

        for start_emu in self.emu_queue:
            worker_q.put(start_emu)
            result_d.setdefault(start_emu.name, start_emu)

        processes: List[multiprocessing.Process] = []
        for n in range(self.core_count):
            p = multiprocessing.Process(target=self._decompose_emu,
                                        args=(
                                            worker_q,
                                            result_d,
                                        ))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        # for emu in self.generated_emus:
        #     print(emu, emu.__dict__)
        for name, emu in result_d.items():
            self.generated_emus.append(emu)

        for index, emus in enumerate(self.generated_emus):
            for emu in emus.sources.values():
                if len(emu['emus']) == 1:
                    pass

    def _decompose_emu(self, worker_q, result_d):
        while not worker_q.empty():
            emu = worker_q.get()
            metabolite = self.model.metabolites[emu.metabolite]

            for source_metabolite, mappings_dict in metabolite.metabolites[
                    'produced_from'].items():
                for current_mapping, mappings in mappings_dict.items():
                    for mapping in mappings:
                        source_atoms = []

                        for index, atom in enumerate(mapping['current'],
                                                     start=1):
                            if index in emu and atom in mapping['other']:

                                source_atoms.append(
                                    mapping['other'].index(atom) + 1)
                        if not source_atoms:
                            continue

                        emu_name = '%s_%s' % (source_metabolite.name, ''.join(
                            str(atom) for atom in source_atoms))
                        source_emu = result_d.get(emu_name)
                        if source_emu is None:
                            source_emu = source_metabolite.get_emu(
                                source_atoms)

                        emu_id = f'{mapping["reaction"]}_{current_mapping}'
                        emu.sources.setdefault(emu_id, {})
                        emu.sources[emu_id].setdefault('emus',
                                                       []).append(source_emu)
                        emu.sources[emu_id].setdefault(
                            'flux',
                            mapping['reaction'].forward if mapping['direction']
                            == 'forward' else mapping['reaction'].reverse)

                        if source_emu.metabolite not in self.substrates and source_emu.name not in result_d:
                            worker_q.put(source_emu)
                            result_d.setdefault(source_emu.name, source_emu)

            result_d[emu.name] = emu

        return True

    def _generate_atoms(self, start: int, stop: int) -> List[int]:
        return [atom for atom in range(start, stop + 1)]

    def _initialize_target_emus(self):
        for metabolite in self.targets:
            if metabolite.atom_count:
                atoms = self._generate_atoms(1, metabolite.atom_count)
                emu = metabolite.get_emu(atoms)

                self.emu_queue.append(emu)
                self.generated_emus.setdefault(len(emu), {}).setdefault(
                    emu, len(self.generated_emus[len(emu)]))

    def _initialize_substrate_emus(self):
        for substrate, tracers in self.substrates.items():
            for tracer in tracers:
                labeling = tracer['labeling']
                purity = float(tracer['purity'])
                enrichment = tracer['enrichment']

                for emus in substrate.emus.values():
                    for emu in emus:
                        emu_labeling = [
                            int(labeling[index])
                            for index in range(len(labeling))
                            if index + 1 in emu.atoms
                        ]

                        mass_increase = sum(emu_labeling)

                        if mass_increase:
                            for mass in range(mass_increase + 1):
                                if mass == mass_increase:
                                    emu.mid[mass] += purity * enrichment
                                elif mass == 0:
                                    emu.mid[mass] += (1.0 -
                                                      purity) * enrichment
                                else:
                                    emu.mid[mass] += 0.0

                        else:
                            emu.mid[0] += 1.0 * enrichment

                        self.substrate_emus.append(emu)
        print(self.substrate_emus)

    def calculate_mids(self):
        for emu_size in sorted(self.generated_emus.keys()):
            emu_network = self.generated_emus[emu_size]
            emu_names = list(emu_network.keys())

            seen_emus = []
            adj_matrix = np.zeros([len(emu_network), len(emu_network)])
            sub_matrix = np.empty((len(emu_network), 0), int)

            for index, emu in enumerate(emu_network.keys()):
                for reaction_name, reaction in emu.sources.items():
                    flux = reaction['flux']
                    source_emus = reaction['emus']
                    if not source_emus:
                        print(emu, reaction, source_emus)
                    elif source_emus[0] not in self.substrate_emus:
                        if len(source_emus) == 1:
                            adj_matrix[index][emu_names.index(
                                source_emus[0])] += flux

                        elif len(source_emus) > 1:
                            for source_emu in source_emus:
                                # print(emu, emu_size, source_emu)
                                adj_matrix[index][emu_names.index(
                                    source_emu)] += flux / len(source_emus)
                    else:
                        if source_emus not in seen_emus:
                            seen_emus.append(source_emus)
                            sub_matrix = np.append(sub_matrix,
                                                   np.zeros(
                                                       [len(emu_network), 1]),
                                                   axis=1)

                        sub_matrix[index][seen_emus.index(source_emus)] -= flux

                    adj_matrix[index][index] -= flux * 1

            substrate_mids = self._calculate_substrate_mids(seen_emus)
            # print(emu_network)
            # print(adj_matrix)
            # np.savetxt("adj_test.csv", adj_matrix, delimiter=",")
            # print(seen_emus)
            # print(sub_matrix)

            # print(substrate_mids)
            try:
                target_mids = np.dot(
                    np.dot(np.linalg.inv(adj_matrix), sub_matrix),
                    substrate_mids)
            except np.linalg.LinAlgError as e:
                print(emu_size)

                for col in np.where(~adj_matrix.any(axis=0))[0]:
                    print('col 0', col, emu_names[col])
                for row in np.where(~adj_matrix.any(axis=1))[0]:
                    print('row 0', row, emu_names[row])

                print('LINALG ERROR', e)
                break

            else:
                for emu, mid in zip(emu_network.keys(), target_mids):
                    emu.mid = mid
            self.substrate_emus += emu_network.keys()

    def _calculate_substrate_mids(self, emus):
        mids = [self._get_mid(emu) for emu in emus]

        max_length = len(max(mids, key=len))

        adjusted_mids = [
            np.concatenate([mid, np.zeros(max_length - len(mid))])
            for mid in mids
        ]

        return np.vstack(adjusted_mids)

    def _get_mid(self, mids):
        mid = mids[0].mid
        for index in range(1, len(mids)):
            mid = np.convolve(mid, mids[index].mid)
        return mid

    def get_mids(self):
        mids = []
        for target in self.targets:
            data = target.emus[target.atom_count][0].mid
            mid = {'name': target.name, 'data': data.tolist()}
            mids.append(mid)

        return mids
