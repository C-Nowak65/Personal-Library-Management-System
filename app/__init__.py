from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .core.views import main as main_blueprint
from .core.models import User, db

bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main_blueprint)

    init_db(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_db(app):
    with app.app_context():
        db.create_all()

