from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np

REVERSIBLE = ['↔', '<=>', '<->', '<>']
PRODUCTS_RIGHT = ['→', '->', '-->', '>']
PRODUCTS_LEFT = ['←', '<-', '<--', '<']


class EMU():
    __slots__ = [
        'metabolite', 'atoms', 'sources', 'next', '_mid', 'name', '_parent',
        'children'
    ]

    def __init__(self, metabolite: str, atoms: List[int]):
        self.metabolite = metabolite
        self.atoms = atoms

        self.sources: Dict[str, Dict[str, float | List[EMU]]] = {}
        self.next: List[Tuple[EMU, str]] = []
        self._mid: List[float] = np.zeros(len(self.atoms) + 1)

        self.name = '%s_%s' % (self.metabolite, ''.join(
            str(atom) for atom in self.atoms))

        self._parent: Optional[EMU] = None
        self.children: List[EMU] = []

    @property
    def parent(self) -> Optional[EMU]:
        if self._parent is not None and self._parent.parent is not None:
            return self._parent.parent
        else:
            return self._parent

    @parent.setter
    def parent(self, value: EMU):
        self._parent = value

    @property
    def mid(self) -> List[float]:
        if self.parent is None:
            return self._mid
        else:
            return self.parent.mid

    @mid.setter
    def mid(self, value: List[float]):
        self._mid = value

    def __len__(self):
        return len(self.atoms)

    def __getitem__(self, position: int):
        return self.atoms[position]

    def __repr__(self):
        return '<EMU object "%s">' % self.name

    def __str__(self):
        return '<EMU object "%s">' % self.name


class Metabolite():
    def __init__(self, name: str, atom_count: Optional[int]):
        self.name = name
        self.atom_count = atom_count

        self.prev: Dict[Metabolite, List[Tuple[str, str, str, Reaction,
                                               bool]]] = {}
        self.next: Dict[Metabolite, List[Tuple[str, str, str, Reaction,
                                               bool]]] = {}

        self.emus: Dict[int, List[EMU]] = {}
        if self.atom_count is not None:
            for i in range(self.atom_count):
                self.emus.setdefault(i + 1, [])

    def _set_metabolite_mapping(self, target: str, metabolite: Metabolite,
                                other_mapping: str, source_mapping: str,
                                direction: str, reaction: Reaction):
        if target == 'next':
            self.next.setdefault(metabolite, []).append(
                (other_mapping, source_mapping, direction, reaction, False))
        else:
            self.prev.setdefault(metabolite, []).append(
                (other_mapping, source_mapping, direction, reaction, False))

    def add_reaction(self, reaction: Reaction,
                     source: Tuple[Metabolite, str | None], reactant: str,
                     metabolites: List[Tuple[Metabolite, str | None]]):
        mappings_to_add: List[Dict[str, str]] = []

        if reactant == 'product' and reaction.products_right:
            mappings_to_add.append({'target': 'prev', 'direction': 'forward'})
            if reaction.reversible:
                mappings_to_add.append({
                    'target': 'next',
                    'direction': 'reverse'
                })
        elif reactant == 'product' and not reaction.products_right:
            mappings_to_add.append({'target': 'prev', 'direction': 'reverse'})
            if reaction.reversible:
                mappings_to_add.append({
                    'target': 'next',
                    'direction': 'forward'
                })

        if reactant == 'substrate' and reaction.products_right:
            mappings_to_add.append({'target': 'next', 'direction': 'forward'})
            if reaction.reversible:
                mappings_to_add.append({
                    'target': 'prev',
                    'direction': 'reverse'
                })
        elif reactant == 'substrate' and not reaction.products_right:
            mappings_to_add.append({'target': 'next', 'direction': 'reverse'})
            if reaction.reversible:
                mappings_to_add.append({
                    'target': 'prev',
                    'direction': 'forward'
                })

        source_mapping = source[1]
        for metabolite in metabolites:
            target_mapping = metabolite[1]
            if source_mapping is not None and target_mapping is not None:
                if ('.' in source_mapping and '.' not in target_mapping) or (
                        '.' not in source_mapping and '.' in target_mapping):
                    continue
                if '.' in source_mapping:
                    source_mapping_new = source_mapping.split('.')
                    target_mapping_new = target_mapping.split('.')
                else:
                    source_mapping_new = source_mapping
                    target_mapping_new = target_mapping

                for atom in source_mapping_new:
                    if atom in target_mapping_new:
                        for to_add in mappings_to_add:
                            self._set_metabolite_mapping(
                                to_add['target'], metabolite[0],
                                target_mapping_new, source_mapping_new,
                                to_add['direction'], reaction)
                        break

    def get_emu(self, atoms: List[int]) -> EMU:
        emu = self._search_emus(atoms)

        if not emu:
            emu = EMU(self.name, atoms)
            self.emus.setdefault(len(atoms), []).append(emu)

        return emu

    def _search_emus(self, atoms: List[int]) -> Optional[EMU]:
        for emu in self.emus[len(atoms)]:
            if emu.atoms == atoms:
                return emu

    def __repr__(self) -> str:
        return '<{0} {1!r}>'.format(self.__class__.__name__, (self.name))

    def __len__(self):
        return self.atom_count


class Reaction:
    def __init__(self,
                 name: str,
                 arrow: str,
                 index: int,
                 left_metabolites: str = '',
                 right_metabolites: str = ''):
        self.name = name
        self.index = index

        self.arrow = arrow
        self.left = left_metabolites
        self.right = right_metabolites

        self.products_right = True
        if self.arrow in REVERSIBLE:
            self.reversible = True
        else:
            self.reversible = False
            if self.arrow in PRODUCTS_LEFT:
                self.products_right = False

        self.forward = None
        self.reverse = None

    def set_flux(self, flux_type: str, first: str, second: str):
        """Identify and set fluxes.

        Args:List[Tuple[Metabolite, str | None]]
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
            self.forward, self.reverse = self._set_net_exchange(
                first_flux, second_flux)

        elif flux_type == 'FORWARD_REVERSE':
            self.forward, self.reverse = (first_flux, second_flux)

    def _set_net_exchange(self, first_flux: float,
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

    def __repr__(self):
        return '<{0} {1!r}>'.format(self.__class__.__name__, (self.name))
