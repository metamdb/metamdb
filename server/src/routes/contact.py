"""Routes for contact."""

from flask import Blueprint, jsonify, request

from src.errors import handler

contact_blueprint = Blueprint('contact', __name__, url_prefix='/api/contact')
contact_blueprint.register_error_handler(handler.InvalidUsage,
                                         handler.handle_invalid_usage)


@contact_blueprint.route('', methods=['POST'])
def contact():
    name: str = request.get_json()['name']
    email: str = request.get_json()['email']
    msg: str = request.get_json()["message"]

    # TODO: handle contact
    print(name, email, msg)

    return jsonify({'contact': 'success'})