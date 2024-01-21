from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort, session
from app import app, db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import LoginForm, RegistrationForm, UpdateaccForm
from app.db_classes import User
import datetime
import secrets
import os
from PIL import Image

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = UpdateaccForm()
    if form.validate_on_submit():
        if form.pp.data:
            random_name = secrets.token_hex(10)
            _, extension = os.path.splitext(form.pp.data.filename)
            image_name = random_name + extension
            image_path = os.path.join(app.root_path, 'static/pp', image_name)
            image_size = (125, 125)
            new_image = Image.open(form.pp.data)
            new_image.thumbnail(image_size)
            new_image.save(image_path)
            current_user.pp = image_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        db.session.commit()
        flash('Změny uloženy', 'success')
        redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
    pp = url_for('static', filename='pp/' + current_user.pp)
    return render_template('account.html', pp=pp, form=form, user=current_user)

#region auth
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')
        flash('Přihlášení se nezdařilo - zkontrolujte email a heslo', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass, account_created=datetime.datetime.now(), name=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Účet pro {form.username.data} byl úspěšně vytvořen', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
#endregion auth