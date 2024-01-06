import os

class Config:
    '''A class to handle all the configurations of the database.'''
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key_for_development')
    SQLALCHEMY_DATABASE_URL = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = 'localhost:5000'
    SESSION_COOKIE_NAME =  'my_session'
    PERMANENT_SESSION_LIFETIME = 86400
    REMEMBER_COOKIE_DURATION = 86400
    
    #OTHER
    FEATURE_FLAG_NEW_FEATURE = True
    DEFAULT_LANGUAGE = 'en'

class ProductionCofig(Config):
    '''Production Specific Configurations.'''
    DEBUG = False

class DevelopmentConfig(Config):
    '''Development Specific Configurations.'''
    DEBUG = True

env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    app_config = ProductionCofig
else:
    app_config = DevelopmentConfig


