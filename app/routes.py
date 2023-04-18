import secrets, os
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image

# Avoid Circular Import
from app.models import User

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/sign-up/', methods = ['GET','POST'])
def sign_up():
    registrationForm = RegistrationForm()
    if registrationForm.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(registrationForm.password.data).decode('utf-8')
        user = User(username = registrationForm.username.data, email = registrationForm.email.data, password = hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created Successfully!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title="Sign Up",register=registrationForm)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if loginForm.validate_on_submit():
        user = User.query.filter_by(email=loginForm.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginForm.password.data):
            login_user(user, remember=loginForm.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',title="Sign in",login=loginForm)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/authentication')
def authentication():
    return render_template('validateOTP.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                            image_file=image_file, form=form)