import numpy as np

from src.components.calculation.simulation import Simulation
from src.components.upload.components import Metabolite, Reaction
from src.components.upload.model import AtomMappingModel


def source(reaction, flux, emus, mode='direct'):
    return {
        'reaction': reaction,
        'direction': 'forward',
        'flux': flux,
        'source_mode': mode,
        'emus': emus
    }


def test_emu_trace_serializes_direct_flux_and_mid_contributions():
    model = AtomMappingModel()
    pyruvate = Metabolite('pyruvate', 2)
    pep = Metabolite('PEP', 2)
    malate = Metabolite('malate', 2)
    unused = Metabolite('unused', 1)
    model.metabolites = {
        metabolite.name: metabolite
        for metabolite in (pyruvate, pep, malate, unused)
    }

    target_emu = pyruvate.get_emu([1, 2])
    pep_emu = pep.get_emu([1, 2])
    malate_emu = malate.get_emu([1, 2])
    unused.get_emu([1])

    pep_emu.mid = np.array([0.2, 0.3, 0.5])
    malate_emu.mid = np.array([0.8, 0.1, 0.1])
    target_emu.mid = pep_emu.mid * 0.9 + malate_emu.mid * 0.1
    target_emu.sources = {
        'pep::forward': source('pep', 9.0, [pep_emu]),
        'malate::forward': source('malate', 1.0, [malate_emu])
    }

    simulation = Simulation(model)
    simulation.targets = [pyruvate]
    simulation.substrates = {pep: [], malate: []}

    trace = simulation.get_emu_trace()
    target = trace['nodes']['pyruvate::1,2']
    rows = {row['reaction']: row for row in target['sources']}

    assert set(trace['nodes']) == {
        'pyruvate::1,2', 'PEP::1,2', 'malate::1,2'
    }
    assert rows['pep']['flux_share'] == 0.9
    assert rows['malate']['flux_share'] == 0.1
    assert np.allclose(
        np.sum([row['mid_contribution'] for row in rows.values()], axis=0),
        target_emu.mid)


def test_emu_trace_convolves_condensation_source_emus():
    model = AtomMappingModel()
    citrate = Metabolite('citrate', 3)
    acetyl_coa = Metabolite('acetyl-CoA', 1)
    oxaloacetate = Metabolite('oxaloacetate', 2)
    model.metabolites = {
        metabolite.name: metabolite
        for metabolite in (citrate, acetyl_coa, oxaloacetate)
    }

    citrate_emu = citrate.get_emu([1, 2, 3])
    acetyl_coa_emu = acetyl_coa.get_emu([1])
    oxaloacetate_emu = oxaloacetate.get_emu([1, 2])
    acetyl_coa_emu.mid = np.array([0.75, 0.25])
    oxaloacetate_emu.mid = np.array([0.5, 0.4, 0.1])
    citrate_emu.mid = np.convolve(acetyl_coa_emu.mid, oxaloacetate_emu.mid)
    citrate_emu.sources = {
        'citrate synthase::forward': source(
            'citrate synthase',
            12.5,
            [acetyl_coa_emu, oxaloacetate_emu],
            'convolution')
    }

    simulation = Simulation(model)
    simulation.targets = [citrate]
    simulation.substrates = {acetyl_coa: [], oxaloacetate: []}

    trace = simulation.get_emu_trace()
    row = trace['nodes']['citrate::1,2,3']['sources'][0]

    assert row['source_mode'] == 'convolution'
    assert row['flux_share'] == 1.0
    assert np.allclose(row['source_mid'], citrate_emu.mid)
    assert np.allclose(row['mid_contribution'], citrate_emu.mid)
    assert [source_emu['id'] for source_emu in row['source_emus']] == [
        'acetyl-CoA::1', 'oxaloacetate::1,2'
    ]


def test_metabolite_network_includes_unmapped_consuming_endpoint():
    model = AtomMappingModel()
    glycine = Metabolite('glycine', 2)
    biomass = Reaction('biomass', '→', 0, 'glycine', 'biomass')
    biomass.forward = 3.5
    biomass.reverse = 0

    glycine.add_reaction(biomass, (glycine, None), 'substrate', [])
    model.metabolites = {'glycine': glycine}
    model.reactions = {'biomass': biomass}

    network = Simulation(model).get_metabolite_network()
    endpoint = network['glycine']['consumed_by'][0]

    assert endpoint == {
        'reaction': 'biomass',
        'direction': 'forward',
        'flux': 3.5,
        'source_metabolite': 'glycine',
        'source_atoms': [1, 2],
        'target_metabolite': None,
        'target_atoms': [],
        'mapped': False,
        'equation': 'glycine → biomass'
    }


def test_decode_retains_unmapped_secretion_before_mapped_reaction():
    model = AtomMappingModel()._decode_metamdb([
        {
            'name': 'glycine secretion',
            'arrow': '→',
            'index': 0,
            'left': 'glycine',
            'right': '',
            'mappings': []
        },
        {
            'name': 'glycine synthesis',
            'arrow': '→',
            'index': 1,
            'left': 'precursor (ab)',
            'right': 'glycine (ab)',
            'mappings': [[
                {
                    'name': 'precursor',
                    'mapping': 'ab',
                    'reactant': 'substrate'
                },
                {
                    'name': 'glycine',
                    'mapping': 'ab',
                    'reactant': 'product'
                }
            ]]
        }
    ])
    model.decode_flux(iter([
        ['glycine secretion', '2.0', '0'],
        ['glycine synthesis', '1.0', '0']
    ]), 'FORWARD_REVERSE')

    network = Simulation(model).get_metabolite_network()

    assert set(model.reactions) == {'glycine secretion', 'glycine synthesis'}
    assert network['glycine']['atom_count'] == 2
    assert network['glycine']['consumed_by'][0]['reaction'] == (
        'glycine secretion')
