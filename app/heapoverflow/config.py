from os import environ, path
#from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
#load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class DevConfig(Config):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True

    # DATABASE
    SQL_USER = 'postgres'
    SQL_PASSWORD = 'stackoverflow'
    #environ.get('SQL_PASSWORD')
    SQL_URI = '127.0.0.1'
    SQL_DB = 'stackoverflow'
    SQL_PORT = '5432'