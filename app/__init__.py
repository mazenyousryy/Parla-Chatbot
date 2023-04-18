from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# __name__ -> name of the module (app.py)
app = Flask(__name__)

# Setting a secret key
app.config['SECRET_KEY'] = '2023PARLA2GRADUATION0PROJECT2023'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parla.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes

# Create DB
with app.app_context():
            db.create_all()