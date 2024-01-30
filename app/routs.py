from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort, session
from werkzeug.utils import secure_filename
from app import app, db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from app import login_manager
from app.forms import LoginForm, RegistrationForm, UpdateaccForm, ItemForm, ItemEditForm
from app.db_classes import User, Item
from app.mail import send_email
import datetime
import secrets
import os
from PIL import Image
from app.utils import generate_unique_folder_hex
from app.decorators import confirmation_required
import shutil
from app import VALID_SUBJECTS, VALID_PROFESSORS

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static/img', 'favicon.ico')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
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

@app.route('/account/items')
@login_required
@confirmation_required
def my_items():
    return render_template('my_items.html', user=current_user)

@app.route('/u/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if not user: abort(404)
    my = True if current_user.id == user.id else False 
    return render_template('profile.html', user=user, my=my)

@app.route('/item/<item_id>')
def view_item(item_id):
    if not item_id.isdigit(): abort(404)
    item_id = int(item_id)
    item = Item.query.get(item_id)
    if not item: abort(404)
    my = False
    if current_user.is_authenticated:
        if item.uploaded_by == current_user.id:
            my = True
    item.author_username = User.query.filter_by(id=item.uploaded_by).first().username
    return render_template('item.html', item=item, my=my)

@app.route('/add', methods=['GET', 'POST'])
@login_required
@confirmation_required
def add_item():
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

        flash('Příspěvek byl přidán', 'success')
        return redirect(url_for('my_items'))
    return render_template('add_item.html', form=form)

@app.route('/edit_item/<item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    if not item_id.isdigit(): abort(404)
    item_id = int(item_id)
    item = Item.query.get(item_id)
    if not item: abort(404)
    if item.uploaded_by != current_user.id: abort(403)
    if not item: abort(404)

    form = ItemEditForm(name=item.name, item_type=item.item_type, tags=item.tags, prof=item.prof, note=item.note, subject=item.subject)
    form.remove_files.choices = filenames = item.filenames.split(";")

    if form.validate_on_submit():
        if form.remove_files.data or form.add_files.data:
            new_filenames = ""
            new_filenames += item.filenames
            if form.remove_files.data:
                filenames = item.filenames.split(";")
                for filename in form.remove_files.data:
                    if filename not in filenames: continue
                    filenames.remove(filename)
                if len(filenames) > 0:
                    new_filenames = ";".join(filenames)
                else:
                    new_filenames = ''
            if form.add_files.data:
                filenames = [secure_filename(file.filename) for file in form.add_files.data if file.filename not in new_filenames]
                filenames_string = ";".join(filenames)
                if len(new_filenames) > 0 and len(filenames) > 0:
                    print('test')
                    new_filenames += ";"
                new_filenames += filenames_string
            if not new_filenames:
                flash('Příspěvek musí mít alespoň jeden soubor. Změny nebyly uloženy.')
                return render_template('edit_item.html', form=form)
            elif len(new_filenames.split(';')) > 5:
                flash('Maximalní počet souborů je 5. Změny nebyly uloženy.', 'danger')
                return render_template('edit_item.html', form=form)
            else:
                item.filenames = new_filenames
                if form.remove_files.data:
                    filenames = item.filenames.split(";")
                    for filename in form.remove_files.data:
                        os.remove(os.path.join(app.root_path, 'static/items', item.folder, secure_filename(filename)))
                if form.add_files.data:
                    for file in form.add_files.data:
                        file.save(os.path.join(app.root_path, 'static/items', item.folder, secure_filename(file.filename)))
        item.name = form.name.data
        item.item_type = form.item_type.data
        item.tags = form.tags.data
        item.prof = form.prof.data
        item.note = form.note.data
        item.subject = form.subject.data

        item.note += f"\n --- \n Editováno {datetime.date.today()}"

        db.session.commit()
        flash('Změny uloženy')
        return redirect(url_for('edit_item', item_id=item_id))
    return render_template('edit_item.html', form=form)

@app.route('/delete_item/<item_id>')
@login_required
def delete_item(item_id):
    if not item_id.isdigit(): abort(404)
    item_id = int(item_id)
    item = Item.query.get(item_id)
    if not item: abort(404)
    if item.uploaded_by != current_user.id: abort(403)
    if not item: abort(404)
    shutil.rmtree(os.path.join(app.root_path, 'static/items', item.folder))
    db.session.delete(item)
    db.session.commit()
    flash('Příspěvek byl smazán', 'success')
    return redirect(url_for('my_items'))

@app.route('/search/query', methods=['POST'])
def search_query():
    q = request.form['q']
    results = set()
    if q:
        if len(q) > 1:
            if 'name' in request.form:
                results.update(Item.query.filter(Item.name.icontains(q)))
            if 'tags' in request.form:
                results.update(Item.query.filter(Item.tags.icontains(q)))
            if 'files' in request.form:
                results.update(Item.query.filter(Item.filenames.icontains(q)))
            if 'note' in request.form:
                results.update(Item.query.filter(Item.note.icontains(q)))
        if request.form['subject']:
            results = {item for item in results if item.subject == request.form['subject']}
        if request.form['prof']:
            results = {item for item in results if item.prof == request.form['prof']}
        for item in results:
            item.author_username = User.query.filter_by(id=item.uploaded_by).first().username
        results = list(results)

        if request.form['sort'] == 'datetime_oldest':
            results.sort(key=lambda item: item.datetime_uploaded)
        elif request.form['sort'] == 'datetime_newest':
            results.sort(key=lambda item: item.datetime_uploaded, reverse=True)
        elif request.form['sort'] == 'subject':
            results.sort(key=lambda item: item.subject)
    return render_template('search_result.html', results=results, q=q)

@app.route('/search')
def search():
    return render_template('search.html', subjects=VALID_SUBJECTS, profs=VALID_PROFESSORS)

#region auth
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Pro zobrazení této stránky se přihlašte', 'danger')
    return redirect('/login?next=' + request.path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            dest = request.args.get('next')
            if dest: return redirect(dest)
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
        token = user.generate_confirmation_token()
        send_email(user.email, 'Potvrzení účtu', 'confirm_account', user=user, token=token)
        flash(f'Na adresu {user.email} byl odeslán mail. Pro aktivaci účtu klikněte na link v mailu.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/confirm/<token>')
@login_required
def confirm_account(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Váš účet byl úspěšně aktivován!', 'success')
    else:
        flash('Aktivační odkaz je neplatný nebo příliš starý', 'danger')
        return redirect(url_for('account_unconfirmed'))
    return redirect(url_for('index'))

@app.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Potvrzení účtu', 'confirm_account', user=current_user, token=token)
    flash(f'Nový email byl odeslán na adresu {current_user.email}')
    return redirect(url_for('index'))

@app.route('/unconfirmed')
def account_unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('index'))
    return render_template('account_unconfirmed.html')
#endregion auth