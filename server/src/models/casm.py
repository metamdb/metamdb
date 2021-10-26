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


class Role(Casm):
    __tablename__ = 'role'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(45), nullable=False, unique=True)


class User(Casm):
    __tablename__ = 'user'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True),
                     default=func.now(),
                     nullable=False)
    orcid: str = db.Column(db.String(100), nullable=False, unique=True)
    role_id: int = db.Column(db.Integer,
                             db.ForeignKey('role.id'),
                             nullable=False)

    role: str = db.relationship('Role')


class Pathway(Casm):
    __tablename__ = 'pathway'

    pw_id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    source = db.Column(db.String(100))

    reactions = db.relationship('PathwayReaction',
                                backref=db.backref('pathways'),
                                lazy='dynamic')


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


class PathwayReaction(Casm):
    __tablename__ = 'pathway_reactions'

    pathway_id: int = db.Column(db.Integer,
                                db.ForeignKey('pathway.pw_id'),
                                primary_key=True,
                                autoincrement=False)
    reaction_id: int = db.Column(db.Integer,
                                 db.ForeignKey('reaction.id'),
                                 primary_key=True,
                                 autoincrement=False)

    reaction = db.relationship('Reaction', back_populates='pathways')
    pathway: Compound = db.relationship('Pathway', back_populates='reactions')


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
    updated_by_id: int = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
    )
    updated_on: str = db.Column(db.DateTime(timezone=True),
                                onupdate=func.now())
    symmetry: bool = db.Column(db.Boolean)

    identifiers = db.relationship('ReactionSource', back_populates='reaction')
    compounds: List[ReactionCompound] = db.relationship(
        'ReactionCompound', back_populates='reaction')
    pathways = db.relationship('PathwayReaction', back_populates='reaction')

    updated_by = db.relationship('User')


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


class Status(Casm):
    __tablename__ = 'status'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(100), nullable=False, unique=True)


class ReactionHistory(Casm):
    __tablename__ = 'reaction_history'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reaction_id: int = db.Column(db.Integer,
                                 db.ForeignKey('reaction.id'),
                                 nullable=False)
    file: str = db.Column(LONGTEXT, nullable=False)
    description: str = db.Column(LONGTEXT, nullable=False)
    updated_by_id: int = db.Column(db.Integer,
                                   db.ForeignKey('user.id'),
                                   nullable=False)
    updated_on: str = db.Column(db.DateTime(timezone=True),
                                nullable=False,
                                default=func.now())
    review_status_id: int = db.Column(db.Integer,
                                      db.ForeignKey('status.id'),
                                      nullable=False,
                                      default='1')
    reviewed_by_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_on: str = db.Column(db.DateTime(timezone=True),
                                 onupdate=func.now())

    review_status = db.relationship('Status')
    updated_by = db.relationship('User', foreign_keys=[updated_by_id])
    reviewed_by = db.relationship('User', foreign_keys=[reviewed_by_id])
    reaction = db.relationship('Reaction')

    @classmethod
    def update_reaction(self, history):
        reaction = Reaction.query.get(history.reaction_id)
        reaction.file = history.file
        reaction.description = history.description
        reaction.updated = True
        reaction.updated_by_id = history.updated_by_id

        db.session.add(reaction)
        db.session.commit()


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
class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role

    id = ma.auto_field()
    name = ma.auto_field()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    name = ma.auto_field()
    orcid = ma.auto_field()
    role = Nested(RoleSchema)


class SourceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Source

    id = ma.auto_field()
    name = ma.auto_field()


class ReactionSourceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReactionSource

    database_identifier = ma.auto_field(data_key='databaseIdentifier')
    source = Nested(SourceSchema)


class ReactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reaction

    id = ma.auto_field()
    formula = ma.auto_field()
    updated = ma.auto_field()
    identifiers = Nested(ReactionSourceSchema, many=True)


class PathwaySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pathway

    pw_id = ma.auto_field()
    source_id = ma.auto_field()
    name = ma.auto_field()
    source = ma.auto_field()


class CompoundSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Compound

    name = ma.auto_field()
    id = ma.auto_field()


class ReactionCompoundSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReactionCompound

    compound = Nested(CompoundSchema)
    position = ma.auto_field()
    reactant = ma.auto_field()
    quantity = ma.auto_field()


class ReactionJsonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reaction

    id = ma.auto_field()
    formula = ma.auto_field()
    updated = ma.auto_field()
    updated_on = ma.auto_field(data_key='updatedOn')

    updated_by = Nested(UserSchema)
    identifiers = Nested(ReactionSourceSchema, many=True)
    compounds = Nested(ReactionCompoundSchema, many=True)

    href = ma.Method('get_href')
    type = ma.Method('get_type')
    external_urls = ma.Method('get_external_urls')

    file = ma.auto_field(data_key='rxnFile')

    def get_href(self, obj):
        if obj.id is None:
            return ''
        return f'https://metamdb.tu-bs.de/api/reactions/{obj.id}'

    def get_type(self, obj):
        return 'reaction'

    def get_external_urls(self, obj):
        external_urls = {}

        if obj.id is not None:
            external_urls.setdefault(
                'metamdb', f'https://metamdb.tu-bs.de/reaction/{obj.id}')
        else:
            external_urls.setdefault('metamdb', '')

        if obj.img is not None:
            external_urls.setdefault(
                'img', f'https://metamdb.tu-bs.de/img/aam/{obj.img}')
        else:
            external_urls.setdefault('img', '')

        return external_urls


class ReactionPathwaySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reaction

    id = ma.auto_field()
    formula = ma.auto_field()
    updated = ma.auto_field()
    updated_on = ma.auto_field(data_key='updatedOn')
    updated_by = ma.auto_field(data_key='updatedBy')

    identifiers = Nested(ReactionSourceSchema, many=True)

    href = ma.Method('get_href')
    type = ma.Method('get_type')

    external_urls = ma.Method('get_external_urls')

    file = ma.auto_field(data_key='rxnFile')
    json = ma.auto_field(data_key='jsonFile')

    def get_href(self, obj):
        if obj.id is None:
            return ''
        return f'https://metamdb.tu-bs.de/api/reactions/{obj.id}'

    def get_type(self, obj):
        return 'reaction'

    def get_external_urls(self, obj):
        external_urls = {}

        if obj.id is not None:
            external_urls.setdefault(
                'metamdb', f'https://metamdb.tu-bs.de/reaction/{obj.id}')
        else:
            external_urls.setdefault('metamdb', '')

        if obj.img is not None:
            external_urls.setdefault(
                'img', f'https://metamdb.tu-bs.de/img/aam/{obj.img}')
        else:
            external_urls.setdefault('img', '')

        return external_urls


class PathwayReactionsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PathwayReaction

    reaction = Nested(ReactionPathwaySchema)


class PathwayJsonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pathway

    pw_id = ma.auto_field()
    source_id = ma.auto_field()
    name = ma.auto_field()
    source = ma.auto_field()

    href = ma.Method('get_href')
    type = ma.Method('get_type')
    external_urls = ma.Method('get_external_urls')

    reactions = Nested(PathwayReactionsSchema, many=True)

    def get_href(self, obj):
        if obj.pw_id is None:
            return ''
        return f'https://metamdb.tu-bs.de/api/pathways/{obj.pw_id}'

    def get_type(self, obj):
        return 'pathway'

    def get_external_urls(self, obj):
        external_urls = {}

        if obj.pw_id is not None:
            external_urls.setdefault(
                'metamdb', f'https://metamdb.tu-bs.de/pathway/{obj.pw_id}')
        else:
            external_urls.setdefault('metamdb', '')

        return external_urls


class StatusSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Status

    id = ma.auto_field()
    name = ma.auto_field()


class ReactionHistorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReactionHistory

    id = ma.auto_field()
    file = ma.auto_field()
    description = ma.auto_field()
    updated_on = ma.auto_field()
    reviewed_on = ma.auto_field()

    reaction = Nested(ReactionSchema)
    updated_by = Nested(UserSchema)
    reviewed_by = Nested(UserSchema)

    review_status = Nested(StatusSchema)


class PathwayAutoCompleteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pathway

    pw_id = ma.auto_field(data_key='id')
    source_id = ma.auto_field(data_key='sourceId')
    name = ma.auto_field()


class ReactionAutoCompleteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReactionSource

    id = ma.auto_field()
    reaction_id = ma.auto_field(data_key='reactionId')
    database_identifier = ma.auto_field(data_key='databaseIdentifier')
    source = Nested(SourceSchema)


class CompoundAutoCompleteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Compound

    id = ma.auto_field()
    name = ma.auto_field()
    inchi = ma.auto_field()
    inchi_short = ma.auto_field(data_key='inchiShort')
    inchi_key = ma.auto_field(data_key='inchiKey')