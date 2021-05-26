# type: ignore
"""Marshmallow Schemas for json serialization."""

from marshmallow import post_load
from src import ma
from src.components.upload.reaction import ReactionModel


class AtomMappingSchema(ma.Schema):
    name = ma.Str()
    metabolite = ma.Str(allow_none=True)
    reactant = ma.Str()
    mapping = ma.Str(default=[], allow_none=True)


class ReactionSchema(ma.Schema):
    name = ma.Str()
    curated = ma.Str()
    arrow = ma.Str()
    mappings = ma.List(ma.List(ma.Nested(AtomMappingSchema)))
    database_identifier = ma.Str()
    index = ma.Int()
    identifier = ma.Int(allow_none=True)

    forward = ma.Float(allow_none=True)
    reverse = ma.Float(allow_none=True)
    reversible = ma.Boolean()

    metabolites = ma.Dict(keys=ma.Str(),
                          values=ma.List(
                              ma.Nested(lambda: MetaboliteSchema(only=(
                                  'identifier', 'name', 'qty', 'elements')))))


class MetaboliteSchema(ma.Schema):
    qty = ma.Float()
    identifier = ma.Str(allow_none=True)
    name = ma.Str()

    elements = ma.List(ma.Dict(keys=ma.Str()))
    reactions = ma.Dict(keys=ma.Str(),
                        values=ma.List(ma.Nested(ReactionSchema())))


class ElementSchema(ma.Schema):
    identifier = ma.Int()
    name = ma.Str()
    symbol = ma.Str()

    metabolites = ma.List(
        ma.Nested(MetaboliteSchema(exclude=('elements', 'reactions'))))


class ModelSchema(ma.Schema):
    reactions = ma.List(ma.Nested(ReactionSchema))
    elements = ma.Dict(keys=ma.Str(), values=ma.Nested(ElementSchema))
    flux_model = ma.Boolean(data_key='isFluxModel')

    @post_load
    def make_model(self, data, **kwargs):
        model = ReactionModel()
        model.load(**data)

        return model
