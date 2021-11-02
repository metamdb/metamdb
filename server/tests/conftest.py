import pytest
from src import create_app, db
from src.models.casm import Pathway, PathwayReaction, Reaction, Source, ReactionSource


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

            db.session.commit()

        yield client
