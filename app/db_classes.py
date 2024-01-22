from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    name = db.Column(db.String(100)) # realny jmeno
    account_created = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(120), unique=True)
    pp = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    items = db.relationship('Item', backref='user')
    admin = db.Column(db.Integer, nullable=False, default=0)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    filenames = db.Column(db.String, nullable=False) # filenames separated by ;
    item_type = db.Column(db.String(10), nullable=False) # zapisky, pl, ucebnice, prezentace...
    author = db.Column(db.String(100)) # autor - default ten kdo nahrava
    tags = db.Column(db.String(200)) # tagy oddeleny proste mezerou
    prof = db.Column(db.String(100)) # ucitel
    datetime_uploaded = db.Column(db.DateTime)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text) # nejaky dodatecny poznamky
    subject = db.Column(db.String(10)) # predmet
    generated_content = db.Column(db.Text) # content rozpoznany ai