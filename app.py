# from flask import Flask, render_template, url_for, flash, redirect
# from flask_sqlalchemy import SQLAlchemy
# from forms import RegistrationForm, LoginForm

# # __name__ -> name of the module (app.py)
# app = Flask(__name__)

# # Setting a secret key
# app.config['SECRET_KEY'] = '2023PARLA2GRADUATION0PROJECT2023'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parla.db'
# db = SQLAlchemy(app)

# # Avoid Circular Import
# from models import User

# @app.route("/")
# @app.route("/index")
# def index():
#     return render_template('index.html')

# @app.route('/sign-up/', methods = ['GET','POST'])
# def sign_up():
#     registrationForm = RegistrationForm()
#     if registrationForm.validate_on_submit():
#         flash(f'Account Created Successfully!','success')
#         return redirect(url_for('home'))
#     return render_template('register.html',title="Sign Up",register=registrationForm)

# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     loginForm = LoginForm()
#     if loginForm.validate_on_submit():
#         if loginForm.email.data == 'admin@blog.com' and loginForm.password.data == 'password123':
#             flash('You have been logged in!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html',title="Sign in",login=loginForm)

# @app.route('/home')
# def home():
#     return render_template('home.html')

# @app.route('/authentication')
# def authentication():
#     return render_template('validateOTP.html')

from app import app

if __name__ == '__main__':
    app.run(debug=True)