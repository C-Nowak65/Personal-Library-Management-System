from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config

app = Flask(__name__)
app.config.from_object(app_config)

#SQLITE config
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///site.db'

if __name__ == '__main__':
    app.run()
