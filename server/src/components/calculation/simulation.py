"""This module implements functionality for reaction models"""
from __future__ import annotations
import os
import multiprocessing
from typing import Dict, List

import numpy as np
from typing_extensions import TypedDict

from src.components.upload.components import EMU, Metabolite
from src.components.upload.model import AtomMappingModel
from src.errors import handler
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

    def initialize_diagnostic_emu(self, metabolite_name: str,
                                  atoms: List[int]):
        """Ensure an atom subset is calculated without adding it to results."""
        metabolite = self.model.metabolites.get(metabolite_name)
        if (metabolite is None or metabolite.atom_count is None or not atoms
                or any(atom < 1 or atom > metabolite.atom_count
                       for atom in atoms)):
            return None

        diagnostic_emu = metabolite.get_emu(sorted(set(atoms)))

        # Tracer/boundary EMUs receive their prescribed MID during substrate
        # initialization. Other EMUs must join the network calculation.
        if metabolite not in self.substrates:
            self.emu_queue.append(diagnostic_emu)
            self.generated_emus.setdefault(
                len(diagnostic_emu), {}).setdefault(
                    diagnostic_emu,
                    len(self.generated_emus[len(diagnostic_emu)]))

        return diagnostic_emu

    def get_metabolite_reactions(self, metabolite_name: str,
                                 atoms: List[int]):
        """Return carbon-resolved reaction directions around an atom subset."""
        metabolite = self.model.metabolites.get(metabolite_name)
        if metabolite is None:
            return {'produced_by': [], 'consumed_by': []}

        def collect(connections, produced):
            reactions = {}
            for other_metabolite, mappings in connections.items():
                for mapping in mappings:
                    other_mapping = mapping[0]
                    selected_mapping = mapping[1]
                    other_atoms = []
                    mapped_selected_atoms = []
                    for atom_position in atoms:
                        if atom_position > len(selected_mapping):
                            continue
                        mapping_atom = selected_mapping[atom_position - 1]
                        if mapping_atom in other_mapping:
                            mapped_selected_atoms.append(atom_position)
                            other_atoms.append(
                                other_mapping.index(mapping_atom) + 1)

                    if not other_atoms:
                        continue

                    direction = mapping[2]
                    reaction = mapping[3]
                    if produced:
                        source_metabolite = other_metabolite.name
                        source_atoms = other_atoms
                        target_metabolite = metabolite.name
                        target_atoms = mapped_selected_atoms
                    else:
                        source_metabolite = metabolite.name
                        source_atoms = mapped_selected_atoms
                        target_metabolite = other_metabolite.name
                        target_atoms = other_atoms

                    key = (reaction.name, direction, source_metabolite,
                           tuple(source_atoms), target_metabolite,
                           tuple(target_atoms))
                    reactions.setdefault(
                        key, {
                            'reaction': reaction.name,
                            'direction': direction,
                            'flux': getattr(reaction, direction),
                            'source_metabolite': source_metabolite,
                            'source_atoms': source_atoms,
                            'target_metabolite': target_metabolite,
                            'target_atoms': target_atoms
                        })

            return sorted(
                reactions.values(),
                key=lambda entry: (entry['reaction'], entry['direction']))

        return {
            'produced_by': collect(metabolite.prev, True),
            'consumed_by': collect(metabolite.next, False)
        }

    def get_metabolite_network(self):
        """Serialize every mapped metabolite and its carbon-resolved edges."""
        network = {}
        for metabolite_name, metabolite in sorted(
                self.model.metabolites.items()):
            if metabolite.atom_count is None:
                continue

            atoms = list(range(1, metabolite.atom_count + 1))
            network[metabolite_name] = {
                'name': metabolite_name,
                'atom_count': metabolite.atom_count,
                **self.get_metabolite_reactions(metabolite_name, atoms)
            }

        return network

    @staticmethod
    def _emu_key(emu: EMU) -> str:
        atoms = ','.join(str(atom) for atom in emu.atoms)
        return f'{emu.metabolite}::{atoms}'

    @staticmethod
    def _mid_values(mid) -> List[float]:
        return [float(value) for value in np.asarray(mid, dtype=float)]

    def _combined_source_mid(self, source_emus: List[EMU],
                             source_mode: str):
        if not source_emus:
            return np.array([], dtype=float)

        if source_mode == 'convolution':
            combined_mid = np.asarray(source_emus[0].mid, dtype=float)
            for source_emu in source_emus[1:]:
                combined_mid = np.convolve(
                    combined_mid,
                    np.asarray(source_emu.mid, dtype=float))
            return combined_mid

        if source_mode == 'average':
            return np.mean([
                np.asarray(source_emu.mid, dtype=float)
                for source_emu in source_emus
            ], axis=0)

        return np.asarray(source_emus[0].mid, dtype=float)

    @staticmethod
    def _fit_mid(mid, size: int):
        mid_values = np.asarray(mid, dtype=float)
        if len(mid_values) < size:
            return np.pad(mid_values, (0, size - len(mid_values)))
        return mid_values[:size]

    def get_emu_trace(self):
        """Serialize the calculated EMU graph required by selected targets."""
        target_emus = []
        for target in self.targets:
            if target.atom_count is None:
                continue
            atoms = list(range(1, target.atom_count + 1))
            target_emus.append(target.get_emu(atoms))

        boundary_metabolites = {
            metabolite.name for metabolite in self.substrates
        }
        nodes = {}
        pending = list(target_emus)

        while pending:
            emu = pending.pop()
            emu_key = self._emu_key(emu)
            if emu_key in nodes:
                continue

            target_mid = np.asarray(emu.mid, dtype=float)
            total_flux = sum(
                float(source.get('flux') or 0.0)
                for source in emu.sources.values())
            source_rows = []

            for source in emu.sources.values():
                source_emus = source.get('emus', [])
                pending.extend(source_emus)

                flux = float(source.get('flux') or 0.0)
                flux_share = flux / total_flux if total_flux else 0.0
                source_mode = source.get('source_mode', 'direct')
                source_mid = self._fit_mid(
                    self._combined_source_mid(source_emus, source_mode),
                    len(target_mid))
                mid_contribution = source_mid * flux_share
                mass_isotopomer_share = np.divide(
                    mid_contribution,
                    target_mid,
                    out=np.zeros_like(mid_contribution),
                    where=np.abs(target_mid) > 1e-15)

                source_rows.append({
                    'reaction': source.get('reaction'),
                    'direction': source.get('direction'),
                    'flux': flux,
                    'flux_share': flux_share,
                    'source_mode': source_mode,
                    'source_mid': self._mid_values(source_mid),
                    'mid_contribution': self._mid_values(mid_contribution),
                    'mass_isotopomer_share': self._mid_values(
                        mass_isotopomer_share),
                    'source_emus': [{
                        'id': self._emu_key(source_emu),
                        'metabolite': source_emu.metabolite,
                        'atoms': source_emu.atoms,
                        'mid': self._mid_values(source_emu.mid)
                    } for source_emu in source_emus]
                })

            source_rows.sort(
                key=lambda row: (row['reaction'] or '',
                                 row['direction'] or ''))
            nodes[emu_key] = {
                'id': emu_key,
                'metabolite': emu.metabolite,
                'atoms': emu.atoms,
                'mid': self._mid_values(target_mid),
                'boundary': (emu.metabolite in boundary_metabolites
                             or not source_rows),
                'sources': source_rows
            }

        return {
            'targets': [{
                'id': self._emu_key(emu),
                'metabolite': emu.metabolite,
                'atoms': emu.atoms
            } for emu in target_emus],
            'nodes': nodes
        }

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
                    emu_id = f'{reaction.name}::{direction}'
                    source_emu = source_metabolite.get_emu(source_atoms)
                    source_emu_len = len(source_emu)
                    self.generated_emus.setdefault(source_emu_len, {})

                    emu.sources.setdefault(emu_id, {})
                    emu.sources[emu_id].setdefault('flux', flux)
                    emu.sources[emu_id].setdefault('emus', [])
                    emu.sources[emu_id].setdefault('reaction', reaction.name)
                    emu.sources[emu_id].setdefault('direction', direction)
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
                            reaction['source_mode'] = 'direct'
                            adj_matrix[index][emu_names.index(
                                source_emus[0])] += flux

                        elif len(source_emus) > 1:
                            reaction['source_mode'] = 'average'
                            for source_emu in source_emus:
                                adj_matrix[index][emu_names.index(
                                    source_emu)] += flux / len(source_emus)
                    else:
                        reaction['source_mode'] = (
                            'convolution'
                            if len(source_emus) > 1 else 'direct')
                        if source_emus not in seen_emus:
                            seen_emus.append(source_emus)
                            sub_matrix = np.append(sub_matrix,
                                                   np.zeros(
                                                       [len(emu_network), 1]),
                                                   axis=1)

                        sub_matrix[index][seen_emus.index(source_emus)] -= flux

                    adj_matrix[index][index] -= flux * 1

            substrate_mids = self._calculate_substrate_mids(seen_emus)

            try:
                target_mids = np.dot(
                    np.dot(np.linalg.inv(adj_matrix), sub_matrix),
                    substrate_mids)
            except np.linalg.LinAlgError as e:
                print(emu_size)

                for col in np.where(~adj_matrix.any(axis=0))[0]:
                    print('col 0', col, emu_names[col])

                zero_row = []
                for row in np.where(~adj_matrix.any(axis=1))[0]:
                    if emu_names[row].metabolite not in zero_row:
                        zero_row.append(emu_names[row].metabolite)
                    print('row 0', row, emu_names[row])
                if zero_row:
                    raise handler.DeadEndError(zero_row)

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
            print(target, [tar.mid for tar in target.emus[1]])
            data = target.emus[target.atom_count][0].mid
            mid = {'name': target.name, 'data': data.tolist()}
            mids.append(mid)

        return mids
