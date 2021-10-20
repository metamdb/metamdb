"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SERVER_PORT = environ.get('SERVER_PORT')
    DB_PORT = environ.get('DB_PORT')

    HOST = environ.get('DB_HOST')
    USER = environ.get('DB_USER')
    PASSWD = environ.get('DB_PASSWD')

    DB = environ.get('DB')
    USER_DB = environ.get('USER_DB')

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}?auth_plugin=mysql_native_password'.format(
        USER, PASSWD, HOST, DB_PORT, DB)

    USER_DATABASE_URI = 'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}?auth_plugin=mysql_native_password'.format(
        USER, PASSWD, HOST, DB_PORT, USER_DB)

    SQLALCHEMY_BINDS = {
        'casm': SQLALCHEMY_DATABASE_URI,
        'casm_user': USER_DATABASE_URI
    }

    WEBSERVER_PORT = environ.get('WEBSERVER_PORT')
    WEBSERVER_HOST = environ.get('WEBSERVER_HOST')
    WEBSERVER_URI = '{0}:{1}'.format(WEBSERVER_HOST, WEBSERVER_PORT)

    ORCID_CLIENT_ID = environ.get('ORCID_CLIENT_ID')
    ORCID_CLIENT_SECRET = environ.get('ORCID_CLIENT_SECRET')
    ORCID_ACCESS_TOKEN_URL = environ.get('ORCID_ACCESS_TOKEN_URL')
    ORCID_AUTHORIZE_URL = environ.get('ORCID_AUTHORIZE_URL')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
