# -*- coding: utf-8 -*-
"""This module generates atom transitions."""

import os
import shutil

from flask import current_app

from src import db
from src.models.casm import Reaction
from src.errors.handler import InvalidUsage

parent = os.path.dirname(os.path.dirname(__file__))
database = '/home/cst/SynologyDrive/casm/casm/server/src/database'
unmapped_directory = os.path.join(database, 'unmapped_reactionfiles')
mapped_directory = os.path.join(database, 'mapped_reactionfiles')

rdt_path = os.path.join(database, 'class/rdt_v220.jar')

img_path = '/home/cst/SynologyDrive/casm/casm/client/public/img'
img_aam_path = os.path.join(img_path, 'AAM')
img_met_path = os.path.join(img_path, 'MET')


def generate_image_for_atom_transition(reaction_id, atom_transition):
    pass


def generate_atom_transition_for_reaction(reaction):
    pass


def update_atom_transition(reaction_id, atom_transition):
    pass


def load_atom_transition(reaction_id):
    for atom_transition in os.listdir(mapped_directory):
        if atom_transition.endswith('.rxn'):
            with open(os.path.join(mapped_directory, atom_transition),
                      'r') as fio:
                name = atom_transition.split('.rxn')[0]

                if name.endswith('_sym'):
                    sym = 1
                else:
                    sym = 0

                return (sym, fio.read())


def load_atom_transitions():
    for atom_transition in os.listdir(mapped_directory):
        if atom_transition.endswith('.rxn'):
            with open(os.path.join(mapped_directory, atom_transition),
                      'r') as fio:
                name = atom_transition.split('.rxn')[0]

                if name.endswith('_sym'):
                    sym = 1
                else:
                    sym = 0

                yield (name, sym, fio.read())


def update_atom_transitions():
    for (name, sym, atom_transition_file) in load_atom_transitions():
        aam = Reaction.query.get(name)

        aam.file = atom_transition_file
        aam.sym = sym
        aam.img = f'{name}.svg'

        db.session.commit()


def clean_up(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        # TODO: error
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def generate_batch_aam(reactions):
    host = current_app.config['HOST']
    user = current_app.config['USER']
    passwd = current_app.config['PASSWD']
    database = current_app.config['DB']


def generate_batch_metabolite(metabolites):
    pass
