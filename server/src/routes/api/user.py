from flask import Blueprint, jsonify
from src.errors import handler
from src.models.casm import ReactionHistory, ReactionHistorySchema, User, UserSchema

from src import bcrypt, db, oauth
from sqlalchemy import func

user_blueprint = Blueprint('user', __name__, url_prefix='/api/user')
user_blueprint.register_error_handler(handler.InvalidUsage,
                                      handler.handle_invalid_usage)


@user_blueprint.route('/<string:id>', methods=['GET'])
def get_user(id):
    history = ReactionHistory.query.filter(
        ReactionHistory.updated_by_id == id).all()
    history_schema = ReactionHistorySchema(many=True)
    history_dump = history_schema.dump(history)

    user = User.query.get(id)
    user_schema = UserSchema()
    user_dump = user_schema.dump(user)

    return jsonify({'user': user_dump, 'history': history_dump})
