"""Routes for the registration and login of users."""

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import create_access_token

from src import bcrypt, db
from src.errors import handler
from src.models import casm_user

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_blueprint.register_error_handler(handler.InvalidUsage,
                                      handler.handle_invalid_usage)


@auth_blueprint.route('/register', methods=['POST'])
def register() -> Response:
    """Register route that registers a user
    provided the email and name are not used already.

    Raises:
        handler.ExistingUser: ExistingUser exception that raises
        a 400 error if the user name already exists.
        handler.ExistingEmail: ExistingEmail exception that raises
        a 400 error if the email already exists.

    Returns:
        Response: Flask Response object with JSON data containing
        the access_token, the user id, and the user name.
    """
    name: str = request.get_json()['name']
    email: str = request.get_json()['email']
    password: str = bcrypt.generate_password_hash(
        request.get_json()['password']).decode('utf-8')

    user_exists: bool = db.session.query(db.session.query().exists().where(
        casm_user.User.name == name)).scalar()
    if user_exists:
        raise handler.ExistingUser()

    email_exists: bool = db.session.query(db.session.query().exists().where(
        casm_user.User.email == email)).scalar()
    if email_exists:
        raise handler.ExistingEmail()

    user: casm_user.User = casm_user.User(name=name,
                                          email=email,
                                          password=password)

    db.session.add(user)
    db.session.commit()

    access_token: str = create_access_token(identity={
        'name': user.name,
        'id': user.id,
        'email': user.email
    })

    response: Response = jsonify({
        'token': access_token,
        'id': user.id,
        'name': user.name
    })
    return response


@auth_blueprint.route('/login', methods=['POST'])
def login() -> Response:
    """Login route that logs in an existing user provided the password is valid.

    Raises:
        handler.InvalidUser: InvalidUser exception raises a 400 error
        if the user doesn't exist.
        handler.InvalidPassword: InvalidPassword exception raises a 400 error
        if the password is wrong.

    Returns:
        Response: Flask Response object with JSON data containing
        the access_token, the user id, and the user name.
    """
    name: str = request.get_json()['name']
    password: str = request.get_json()['password']

    user: casm_user.User = casm_user.User.query.filter(
        casm_user.User.name == name).first()

    if not user:
        raise handler.InvalidUser()

    if not bcrypt.check_password_hash(user.password, password):
        raise handler.InvalidPassword()

    access_token: str = create_access_token(identity={
        'name': user.name,
        'id': user.id,
        'email': user.email
    })

    response: Response = jsonify({
        'token': access_token,
        'id': user.id,
        'name': user.name
    })
    return response
