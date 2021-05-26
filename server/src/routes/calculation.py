"""Routes for the calculation of mid labelings."""

import json
from typing import List, TYPE_CHECKING

from flask import Blueprint, Response, jsonify, request
from src.components.calculation import emu
from src.components.upload.reaction import ReactionModel
from src.errors import handler
from src.validation import calculation as calc_validation

if TYPE_CHECKING:
    from typings.casm.calculation import CalcData, ReactionTyping, TracerTyping

calculation_blueprint = Blueprint('calc',
                                  __name__,
                                  url_prefix='/api/calculation')
calculation_blueprint.register_error_handler(handler.InvalidUsage,
                                             handler.handle_invalid_usage)


@calculation_blueprint.route('', methods=['POST'])
def calculate_mids() -> Response:
    data: "CalcData" = request.form.to_dict()

    is_error, errors = calc_validation.validate_calculation(data)

    if is_error and errors is not None:
        raise handler.InvalidUsage(status_code=400, payload=errors)

    model_data: "List[ReactionTyping]" = json.loads(data['model'])
    model = ReactionModel()
    model.load(model_data)

    tracer: "TracerTyping" = json.loads(data['tracer'])
    products: List[str] = json.loads(data['products'])

    emu_model = emu.Model(model, tracer, products, data['element'])
    emu_model.calculate_mids()
    mids = emu_model.get_mids()

    response: Response = jsonify(mids)
    return response
