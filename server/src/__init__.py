# type: ignore
import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
oauth = OAuth()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    flask_config = os.getenv('FLASK_CONFIG')
    if flask_config:
        app.config.from_object('config.' + flask_config)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    oauth.init_app(app)
    jwt.init_app(app)

    orcid = oauth.register(
        name='orcid',
        client_id=app.config["ORCID_CLIENT_ID"],
        client_secret=app.config["ORCID_CLIENT_SECRET"],
        access_token_url=app.config["ORCID_ACCESS_TOKEN_URL"],
        access_token_params=None,
        authorize_url=app.config["ORCID_AUTHORIZE_URL"],
        authorize_params=None,
        client_kwargs={'scope': '/authenticate'},
    )

    CORS(app, resources={r'/api/*': {'origins': app.config['WEBSERVER_URI']}})

    from src.routes.calculation import calculation_blueprint
    app.register_blueprint(calculation_blueprint)

    from src.routes.query import query_blueprint
    app.register_blueprint(query_blueprint)

    from src.routes.transition import transition_blueprint
    app.register_blueprint(transition_blueprint)

    from src.routes.upload import upload_blueprint
    app.register_blueprint(upload_blueprint)

    from src.routes.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from src.routes.test import test_blueprint
    app.register_blueprint(test_blueprint)

    from src.routes.contact import contact_blueprint
    app.register_blueprint(contact_blueprint)

    from src.routes.api.reactions import reactions_blueprint
    app.register_blueprint(reactions_blueprint)

    from src.routes.api.search import search_blueprint
    app.register_blueprint(search_blueprint)

    from src.routes.api.pathways import pathways_blueprint
    app.register_blueprint(pathways_blueprint)

    from src.routes.api.user import user_blueprint
    app.register_blueprint(user_blueprint)

    from src.routes.review import review_blueprint
    app.register_blueprint(review_blueprint)

    from src.routes.suggestions import suggestions_blueprint
    app.register_blueprint(suggestions_blueprint)

    return app
