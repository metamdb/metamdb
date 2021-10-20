"""Routes for the registration and login of users."""

from os import stat
from flask import Blueprint, jsonify, url_for, redirect, current_app
from flask_jwt_extended import create_access_token, jwt_required, current_user
from werkzeug.exceptions import BadRequestKeyError

from src import db, oauth, jwt
from src.errors import handler
from src.models.casm import User, ReactionHistory, ReactionHistorySchema

import datetime

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_blueprint.register_error_handler(handler.InvalidUsage,
                                      handler.handle_invalid_usage)

APPROVED_REVIEWERS = [2, 3]


@auth_blueprint.route('/orcid', methods=['GET'])
def orcid_login():
    orcid = oauth.create_client('orcid')
    redirect_uri = url_for('auth.orcid_authorize', _external=True)

    return orcid.authorize_redirect(redirect_uri)


@auth_blueprint.route('/orcid/authorize', methods=['GET'])
def orcid_authorize():
    WEBSERVER_URI = current_app.config["WEBSERVER_URI"]
    orcid = oauth.create_client('orcid')
    try:
        token = orcid.authorize_access_token()
    except BadRequestKeyError:
        return redirect(f'{WEBSERVER_URI}/postLogin', 400)
    else:
        if not token:
            raise handler.InvalidToken()

    token_name = token['name']
    token_orcid = token['orcid']

    user: User = User.query.filter(User.orcid == token_orcid).first()

    if user is None:
        user: User = User(name=token_name, orcid=token_orcid, role_id=1)

        db.session.add(user)
        db.session.commit()
        print('Creating user: ', user)

    access_token: str = create_access_token(
        identity={
            'name': user.name,
            'orcid': user.orcid,
            'id': user.id,
            'role': user.role_id
        },
        expires_delta=datetime.timedelta(days=1))

    return redirect(f'{WEBSERVER_URI}/postLogin?jwt={access_token}')


@auth_blueprint.route('/me', methods=['GET'])
@jwt_required()
def get_user_data():
    history_schema = ReactionHistorySchema(many=True)

    history = ReactionHistory.query.filter(
        ReactionHistory.updated_by_id == current_user.id).all()
    history_dump = history_schema.dump(history)

    if current_user.role_id in APPROVED_REVIEWERS:
        review = ReactionHistory.query.filter(
            ReactionHistory.review_status_id == 1).all()
        review_dump = history_schema.dump(review)
    else:
        review_dump = None

    return jsonify({'history': history_dump, 'reviews': review_dump})


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]

    return User.query.get(identity['id'])