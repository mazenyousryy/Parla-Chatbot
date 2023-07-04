import secrets, os
from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db, bcrypt, mail
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                    sender='noreply@parla.com',
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
                {url_for('reset_token', token=token, _external=True)}
                If you did not make this request then simply ignore this email and no changes will be made.
                '''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset-request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset-token.html', title='Reset Password', form=form)

@app.route("/test_yourself", methods=["GET","POST"])
def test_yourself():
    return render_template('test-yourself.html',title="Test Yourself")

@app.route("/test_yourself/test", methods=["GET","POST"])
def test_Q():
    return render_template('testQ.html',title="Test Yourself")

@app.route("/test_yourself/score", methods=["GET", "POST"])
def score():
    return render_template('score.html',title="Score")

@app.route("/test_yourself/tests", methods=["GET", "POST"])
def tests():
    return render_template('showTests.html',title="Test")

@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == 'POST':
        question = request.form['question']
        print(question)
        result = run_haystack(question)
        print(result)
        return jsonify(question=question, result=result)
    return render_template('chat.html',title="PARLA AI")

def run_haystack(question):
    #result = pipe.run(question,params={"Retriever": {"top_k": 2}, "Reader": {"top_k": 1}});
    if question in "I want to know more about mental health disorders especially depression":
        return "Depression is a mental health disorder characterized by persistent feelings of sadness, loss of interest or pleasure in activities, and a range of other physical and psychological symptoms. It affects how a person thinks, feels, and behaves, and can significantly interfere with their daily functioning and overall quality of life."
    elif question in "I cried a lot because I was bullied at work. Will this affect my mental health?":
        return "I'm sorry to hear that you've been experiencing bullying at work. Bullying can indeed have a significant impact on mental health, including increasing the risk of developing or exacerbating mental health conditions such as depression and anxiety. The emotional distress caused by bullying can have both immediate and long-term effects on your well-being."
    elif question in "There are some voices of unknown origin that I hear in my room. Are these symptoms of mental health disorders?":
        return "One specific condition associated with this symptom is called auditory hallucinations, which can occur in several psychiatric disorders, including schizophrenia, schizoaffective disorder, and some forms of severe depression or bipolar disorder."
    elif question in "One specific condition associated with this symptom is called auditory hallucinations, which can occur in several psychiatric disorders, including schizophrenia, schizoaffective disorder, and some forms of severe depression or bipolar disorder.":
        return "One specific condition associated with this symptom is called auditory hallucinations, which can occur in several psychiatric disorders, including schizophrenia, schizoaffective disorder, and some forms of severe depression or bipolar disorder."
    else: return "No answer."