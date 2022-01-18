import pytest
import datetime
from src import create_app, db
from src.models.casm import Pathway, PathwayReaction, Reaction, Source, ReactionSource, Compound, ReactionCompound, Role, User, Status, ReactionHistory


@pytest.fixture
def client():
    app = create_app('TestConfig')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            pathway1 = Pathway(pw_id=1,
                               source_id='pw_gly',
                               name='glycolysis',
                               source='brenda')
            db.session.add(pathway1)
            pathway2 = Pathway(pw_id=2,
                               source_id='TCA-CYCLE',
                               name='Citric acid cycle',
                               source='metacyc')
            db.session.add(pathway2)
            pathway3 = Pathway(pw_id=3,
                               source_id='pw_cit',
                               name='cit',
                               source='brenda')
            db.session.add(pathway3)
            pathway4 = Pathway(pw_id=4,
                               source_id='rxn-gly',
                               name='gly',
                               source='metacyc')
            db.session.add(pathway4)
            pathway5 = Pathway(pw_id=5,
                               source_id='pw_ala',
                               name='alanine',
                               source='brenda')
            db.session.add(pathway5)
            pathway6 = Pathway(pw_id=6,
                               source_id='rxn-ala',
                               name='alanine',
                               source='metacyc')
            db.session.add(pathway6)
            pathway7 = Pathway(pw_id=7,
                               source_id='pw_leu',
                               name='leucine',
                               source='brenda')
            db.session.add(pathway7)
            pathway8 = Pathway(pw_id=8,
                               source_id='rxn-leu',
                               name='leucine',
                               source='metacyc')
            db.session.add(pathway8)
            pathway9 = Pathway(pw_id=9,
                               source_id='pw_iso',
                               name='iso',
                               source='brenda')
            db.session.add(pathway9)
            pathway10 = Pathway(pw_id=10,
                                source_id='rxn-iso',
                                name='iso',
                                source='metacyc')
            db.session.add(pathway10)
            pathway11 = Pathway(pw_id=11,
                                source_id='pw_met',
                                name='met',
                                source='brenda')
            db.session.add(pathway11)
            pathway12 = Pathway(pw_id=12,
                                source_id='rxn-met',
                                name='met',
                                source='metacyc')
            db.session.add(pathway12)
            pathway13 = Pathway(pw_id=13,
                                source_id='pw_cas',
                                name='cas',
                                source='brenda')
            db.session.add(pathway13)
            pathway14 = Pathway(pw_id=14,
                                source_id='rxn-cas',
                                name='cas',
                                source='metacyc')
            db.session.add(pathway14)
            reaction1 = Reaction(id=1,
                                 formula='succinate <=> fumarate',
                                 natural_substrates=1,
                                 file='LARGE RXN FILE',
                                 json={},
                                 img='1',
                                 updated=0,
                                 updated_by_id=None,
                                 updated_on=None,
                                 symmetry=1,
                                 balanced=0)
            db.session.add(reaction1)
            reaction2 = Reaction(id=2,
                                 formula='malate <=> fumarate',
                                 natural_substrates=1,
                                 file='LARGE RXN FILE',
                                 json={},
                                 img='2',
                                 updated=1,
                                 updated_by_id=1,
                                 updated_on=None,
                                 symmetry=1,
                                 balanced=0)
            db.session.add(reaction2)
            source1 = Source(id=1, name='metacyc')
            db.session.add(source1)
            reaction_souce1 = ReactionSource(
                id=1,
                reaction_id=1,
                source_id=1,
                database_identifier='SUC-FUM-OX-RXN')
            db.session.add(reaction_souce1)
            reaction_souce2 = ReactionSource(id=2,
                                             reaction_id=2,
                                             source_id=1,
                                             database_identifier='RXN-0543')
            db.session.add(reaction_souce2)
            pathway_reaction1 = PathwayReaction(pathway_id=2, reaction_id=1)
            db.session.add(pathway_reaction1)
            compound1 = Compound(
                id=1,
                name='fumarate',
                inchi=
                'InChI=1S/C4H4O4/c5-3(6)1-2-4(7)8/h1-2H,(H,5,6)(H,7,8)/b2-1+',
                inchi_short=
                'C4H4O4/c5-3(6)1-2-4(7)8/h1-2H,(H,5,6)(H,7,8)/b2-1+',
                inchi_key='InChIKey=VZCYOOQTPOCHFL-OWOJBTEDSA-N',
                formula='C4H4O4',
                file='LARGE MOL FILE')
            db.session.add(compound1)
            reaction_compound1 = ReactionCompound(reaction_id=1,
                                                  compound_id=1,
                                                  position=1,
                                                  reactant='substrate',
                                                  quantity=1)
            db.session.add(reaction_compound1)
            role1 = Role(id=1, name='Reviewer')
            db.session.add(role1)
            user1 = User(id=1,
                         name='Test Name',
                         date=None,
                         orcid='0000-0000-1234-5678',
                         role_id=1)
            db.session.add(user1)
            status1 = Status(id=2, name='Approved')
            db.session.add(status1)
            history1 = ReactionHistory(id=1,
                                       reaction_id=1,
                                       file='LARGE RXN FILE 2',
                                       description='Changed to number 2',
                                       updated_by_id=1,
                                       updated_on=None,
                                       review_status_id=2,
                                       reviewed_by_id=1,
                                       reviewed_on=None)
            db.session.add(history1)

            db.session.commit()

        yield client
