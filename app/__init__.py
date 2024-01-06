from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache
from flask_login import LoginManager
from app.core.models import User

db = SQLAlchemy()
cache = Cache()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    register_database(app)
    init_login(app)

    return app

def register_database(app):
    db.init_app(app)
    cache.init_app(app)

def init_login(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

