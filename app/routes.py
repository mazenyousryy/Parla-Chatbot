import secrets, os
from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db, bcrypt, mail
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from PIL import Image
from haystack.nodes import FARMReader,BM25Retriever
from haystack.document_stores import ElasticsearchDocumentStore
from flask import Flask,request,render_template,jsonify
import pandas as pd
from haystack.pipelines import ExtractiveQAPipeline


# Avoid Circular Import
from app.models import User

with open("AllData.csv", 'r') as file:
  df=pd.read_csv('AllData.csv', encoding='Windows-1252')

import pandas as pd
data_json = df.to_dict("records")
print(data_json)
###################################################################################################
doc=ElasticsearchDocumentStore(host="localhost",port="9200")
doc.write_documents(data_json)


ret=BM25Retriever(document_store=doc)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True,num_processes=0)


pipe=ExtractiveQAPipeline(reader,ret)

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
    result = pipe.run(question,params={"Retriever": {"top_k": 2}, "Reader": {"top_k": 1}});
    if result and len(result["answers"]) > 0:
        answer = result["answers"][0].answer
        return answer
    return "No answer found."