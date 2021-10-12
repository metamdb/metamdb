"""Routes for the registration and login of users."""

from flask import Blueprint, Response, jsonify, request, url_for, redirect
from flask_jwt_extended import create_access_token

from src import bcrypt, db, oauth
from src.errors import handler
from src.models import casm_user

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_blueprint.register_error_handler(handler.InvalidUsage,
                                      handler.handle_invalid_usage)

orcid = oauth.register(
    name='orcid',
    client_id='APP-DQ99FS5QEUJ7H6WV',
    client_secret='7357276d-3724-4c5c-a41c-54ee615a12ba',
    access_token_url='https://sandbox.orcid.org/oauth/token',
    access_token_params=None,
    authorize_url='https://sandbox.orcid.org/oauth/authorize',
    authorize_params=None,
    client_kwargs={'scope': '/read-limited /activities/update /person/update'},
)


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


@auth_blueprint.route('/orcid', methods=['GET'])
def orcid_login():
    orcid = oauth.create_client('orcid')
    redirect_uri = url_for('auth.orcid_authorize', _external=True)

    return jsonify(orcid.authorize_redirect(redirect_uri).headers._list)


@auth_blueprint.route('/login/orcid/authorize', methods=['GET'])
def orcid_authorize():
    orcid = oauth.create_client('orcid')

    token = orcid.authorize_access_token()
    print(token, flush=True)

    # resp.raise_for_status()
    # profile = resp.json()
    # print(profile)
    # do something with the token and profile
    return redirect('/')