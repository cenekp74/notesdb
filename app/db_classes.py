from app import db, login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100)) # realny jmeno
    account_created = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(120), unique=True)
    pp = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    items = db.relationship('Item', backref='user')
    admin = db.Column(db.Integer, nullable=False, default=0)
    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.email, salt=current_app.config["SECURITY_PASSWORD_SALT"])
    
    def validate_token(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(
                token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
            )
            if not email == self.email:
                return False
            return True
        except:
            return False
    def confirm(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(
                token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
            )
            if not email == self.email:
                return False
            self.confirmed = True
            db.session.add(self)
            return True
        except:
            return False
        

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    folder = db.Column(db.String(6), nullable=False, unique=True)
    filenames = db.Column(db.String, nullable=False) # filenames separated by ;
    item_type = db.Column(db.String(10), nullable=False) # zapisky, pl, ucebnice, prezentace...
    tags = db.Column(db.String(200)) # tagy oddeleny proste mezerou
    prof = db.Column(db.String(100)) # ucitel
    datetime_uploaded = db.Column(db.DateTime)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text) # nejaky dodatecny poznamky
    subject = db.Column(db.String(10)) # predmet
    generated_content = db.Column(db.Text) # content rozpoznany ai