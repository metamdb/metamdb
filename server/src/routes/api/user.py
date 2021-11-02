from flask import Blueprint, jsonify
from src.errors import handler
from src.models.casm import (ReactionHistory, ReactionHistorySchema, User,
                             UserSchema)
from sqlalchemy import and_

user_blueprint = Blueprint('user', __name__, url_prefix='/api/user')
user_blueprint.register_error_handler(handler.InvalidUsage,
                                      handler.handle_invalid_usage)


@user_blueprint.route('/<string:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user is None:
        raise handler.InvalidId()

    user_schema = UserSchema()
    user_dump = user_schema.dump(user)

    history = ReactionHistory.query.filter(
        and_(ReactionHistory.updated_by_id == id,
             ReactionHistory.review_status_id == 2)).all()
    history_schema = ReactionHistorySchema(
        many=True,
        exclude=('updated_on', 'reviewed_on', 'updated_by', 'reviewed_by'))
    history_dump = history_schema.dump(history)

    return jsonify({'user': user_dump, 'history': history_dump})
