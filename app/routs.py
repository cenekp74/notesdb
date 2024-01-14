from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort, session
from app import app, db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import LoginForm
from app.db_classes import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#region login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')
        flash('Přihlášení se nezdařilo - zkontrolujte email a heslo', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
#endregion login