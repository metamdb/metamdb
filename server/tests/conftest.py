import pytest
import datetime
from src import create_app, db
from src.models.casm import Pathway, PathwayReaction, Reaction, Source, ReactionSource, Compound, ReactionCompound, Role, User


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
            reaction1 = Reaction(id=1,
                                 formula='succinate <=> fumarate',
                                 natural_substrates=1,
                                 file='LARGE RXN FILE',
                                 json={},
                                 img='1',
                                 updated=0,
                                 updated_by_id=None,
                                 updated_on=None,
                                 symmetry=1)
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
                                 symmetry=1)
            db.session.add(reaction2)
            source1 = Source(id=1, name='metacyc')
            db.session.add(source1)
            reaction_souce1 = ReactionSource(
                id=1,
                reaction_id=1,
                source_id=1,
                database_identifier='SUC-FUM-OX-RXN')
            db.session.add(reaction_souce1)
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

            db.session.commit()

        yield client
