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


def create_app():
    app = Flask(__name__)

    flask_config = os.getenv('FLASK_CONFIG')
    if flask_config:
        app.config.from_object('config.' + flask_config)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    oauth.init_app(app)

    CORS(app, resources={r'/api/*': {'origins': app.config['WEBSERVER_URI']}})
    JWTManager(app)

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

    return app
