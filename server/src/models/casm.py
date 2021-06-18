# type: ignore
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from typings.casm.reaction import AtomTransitionTyping

from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import func
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT
from src import db, ma


class Casm(db.Model):
    __abstract__ = True
    __bind_key__ = 'casm'


class Enzyme(Casm):
    __tablename__ = 'enzyme'

    id = db.Column(db.Integer, primary_key=True)
    ec_number = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)


class Compound(Casm):
    __tablename__ = 'compound'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(TEXT)
    inchi: str = db.Column(TEXT)
    inchi_short: str = db.Column(TEXT)
    inchi_key: str = db.Column(db.String(100))
    formula: str = db.Column(TEXT)
    file: str = db.Column(LONGTEXT)

    elements = db.relationship('CompoundElement', back_populates='compound')
    reactions = db.relationship('ReactionCompound',
                                backref=db.backref('compounds'),
                                lazy='dynamic')
    identifiers = db.relationship('CompoundSource', back_populates='compound')


class ReactionCompound(Casm):
    __tablename__ = 'reaction_compounds'

    reaction_id: int = db.Column(db.Integer,
                                 db.ForeignKey('reaction.id'),
                                 primary_key=True,
                                 autoincrement=False)
    compound_id: int = db.Column(db.Integer,
                                 db.ForeignKey('compound.id'),
                                 primary_key=True,
                                 autoincrement=False)
    position: int = db.Column(db.Integer,
                              primary_key=True,
                              autoincrement=False)
    reactant: str = db.Column(db.String(9),
                              primary_key=True,
                              autoincrement=False)
    quantity: int = db.Column(db.Integer, nullable=False)

    reaction = db.relationship('Reaction', back_populates='compounds')
    compound: Compound = db.relationship('Compound',
                                         back_populates='reactions')


class Reaction(Casm):
    __tablename__ = 'reaction'

    id: int = db.Column(db.Integer, primary_key=True)
    formula: str = db.Column(TEXT, nullable=False)
    natural_substrates: bool = db.Column(db.Boolean)
    file: str = db.Column(LONGTEXT)
    json: "AtomTransitionTyping" = db.Column(db.JSON)
    img: str = db.Column(db.String(100))
    description: str = db.Column(LONGTEXT)
    updated: bool = db.Column(db.Boolean)
    updated_by: str = db.Column(db.String(100))
    updated_on: str = db.Column(db.DateTime(timezone=True),
                                onupdate=func.now())
    symmetry: bool = db.Column(db.Boolean)

    identifiers = db.relationship('ReactionSource', back_populates='reaction')
    compounds: List[ReactionCompound] = db.relationship(
        'ReactionCompound', back_populates='reaction')


class Element(Casm):
    __tablename__ = 'element'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    symbol = db.Column(db.String(2), unique=True, nullable=False)

    compounds = db.relationship('CompoundElement', back_populates='element')


class Source(Casm):
    __tablename__ = 'source'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), unique=True, nullable=False)

    reaction = db.relationship('ReactionSource', back_populates='source')
    compound = db.relationship('CompoundSource', back_populates='source')


# ---------- Link Tables ---------- #
class EnzymeReaction(Casm):
    __tablename__ = 'enzyme_reactions'

    enzyme_id = db.Column(db.Integer,
                          db.ForeignKey('enzyme.id'),
                          primary_key=True,
                          autoincrement=False)
    reaction_id = db.Column(db.Integer,
                            db.ForeignKey('reaction.id'),
                            primary_key=True,
                            autoincrement=False)


class ReactionSource(Casm):
    __tablename__ = 'reaction_source'

    id = db.Column(db.Integer, primary_key=True)
    reaction_id = db.Column(db.Integer, db.ForeignKey('reaction.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    database_identifier = db.Column(db.String(100),
                                    unique=True,
                                    nullable=False)

    reaction = db.relationship('Reaction', back_populates="identifiers")
    source = db.relationship('Source', back_populates='reaction')


class CompoundSource(Casm):
    __tablename__ = 'compound_source'

    id = db.Column(db.Integer, primary_key=True)
    compound_id = db.Column(db.Integer, db.ForeignKey('compound.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    database_identifier = db.Column(db.String(500),
                                    unique=True,
                                    nullable=False)
    name = db.Column(TEXT)

    compound = db.relationship('Compound', back_populates='identifiers')
    source = db.relationship('Source', back_populates='compound')


class CompoundElement(Casm):
    __tablename__ = 'compound_elements'

    compound_id = db.Column(db.Integer,
                            db.ForeignKey('compound.id'),
                            primary_key=True,
                            autoincrement=False)
    element_id = db.Column(db.Integer,
                           db.ForeignKey('element.id'),
                           primary_key=True,
                           autoincrement=False)
    quantity = db.Column(db.Integer, nullable=False)

    compound = db.relationship('Compound', back_populates='elements')
    element = db.relationship('Element', back_populates='compounds')


############################# SCHEMAS #############################
class ReactionSourceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReactionSource

    database_identifier = ma.auto_field()


class ReactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reaction

    id = ma.auto_field()
    formula = ma.auto_field()
    updated = ma.auto_field()
    identifiers = Nested(ReactionSourceSchema, many=True)
