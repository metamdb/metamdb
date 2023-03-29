# type: ignore
"""Marshmallow Schemas for json serialization."""

from marshmallow import post_load
from marshmallow.exceptions import ValidationError
from src import ma
from src.components.upload.reaction import ReactionModel
from typing import List, Mapping, Any


class KeyField(ma.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, int) or isinstance(value, float):
            return value
        else:
            raise ValidationError('Field should be int or float')


class ValueField(ma.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, int) or isinstance(value, list):
            return value
        else:
            raise ValidationError('Field should be int or list')


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
    left = ma.Str()
    right = ma.Str()

    reversible = ma.Boolean()
    conversion = ma.Dict(keys=KeyField(), values=ValueField(), allow_none=True)

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
    metabolites = ma.Method('get_metabolites')

    def get_metabolites(self, obj):
        return [val.name for val in obj.metabolites.values()]

    @post_load
    def make_model(self, data, **kwargs):
        model = ReactionModel()
        model.load(**data)

        return model


class ModelReaction(ma.Schema):
    name = ma.Str()
    forward = ma.Float()
    reverse = ma.Float()
    reversible = ma.Boolean()
    arrow = ma.Str()
    left = ma.Str()
    right = ma.Str()


class AtomMappingModelSchema(ma.Schema):
    reactions = ma.List(ma.Nested(ModelReaction))
