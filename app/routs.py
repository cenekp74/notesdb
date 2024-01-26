from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort, session
from werkzeug.utils import secure_filename
from app import app, db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import LoginForm, RegistrationForm, UpdateaccForm, ItemForm
from app.db_classes import User, Item
import datetime
import secrets
import os
from PIL import Image
from app.utils import generate_unique_folder_hex
import time

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
            new_image = new_image.resize(image_size)
            new_image.save(image_path)
            os.remove(os.path.join(app.root_path, 'static/pp', current_user.pp))
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

@app.route('/item/<item_id>')
def view_item(item_id):
    item = Item.query.get(int(item_id))
    if not item: abort(404)
    item.author_username = User.query.filter_by(id=item.uploaded_by).first().username
    return render_template('item.html', item=item)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if not current_user.is_authenticated:
        flash('Pro přidání příspěvku se přihlašte')
        return redirect(url_for('login'))
    form = ItemForm()
    if form.validate_on_submit():
        filenames = [secure_filename(file.filename) for file in form.files.data]
        filenames_string = ";".join(filenames)
        folder = generate_unique_folder_hex()
        os.mkdir(os.path.join(app.root_path, 'static/items', folder))
        for file in form.files.data:
            file.save(os.path.join(app.root_path, 'static/items', folder, secure_filename(file.filename)))

        item = Item(
            name = form.name.data,
            folder = folder,
            item_type = form.item_type.data,
            tags = form.tags.data,
            prof = form.prof.data,
            datetime_uploaded = datetime.datetime.now(),
            note = form.note.data,
            subject = form.subject.data,
            filenames = filenames_string,
            uploaded_by = current_user.id,
        )
        db.session.add(item)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_item.html', form=form)

@app.route('/search/basic/query', methods=['POST'])
def basic_search_query():
    q = request.form['q']
    results = []
    if q:
        if len(q) > 1:
            results.extend(Item.query.filter(Item.name.icontains(q)))
        for item in results:
            item.author_username = User.query.filter_by(id=item.uploaded_by).first().username
    return render_template('search_result.html', results=results, q=q)

@app.route('/search')
def search():
    return render_template('search.html')

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