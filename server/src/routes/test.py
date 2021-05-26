"""Routes for testing."""

from flask import Blueprint, jsonify

test_blueprint = Blueprint('test', __name__, url_prefix='/api/test')


@test_blueprint.route('', methods=['GET'])
def test():
    return jsonify({'test': 'success'})