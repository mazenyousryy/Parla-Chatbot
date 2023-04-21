from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


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

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "parla.chatbot.eg@gmail.com"
app.config['MAIL_PASSWORD'] = "yjxtaarkuljecebg"
mail = Mail(app)

from app import routes

# Create DB
with app.app_context():
            db.create_all()