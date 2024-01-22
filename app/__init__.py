from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

VALID_ITEM_TYPES = ['Zápisky', 'Učebnice', 'Prezentace', 'Jiné']
VALID_SUBJECTS = ['', 'Český jazyk a literatura', 'Matematika', 'Biologie', 'Geografie (zeměpis)', 'Dějepis', 'Anglický jazyk', 'Francouzský jazyk', 'Německý jazyk', 'Fyzika', 'Chemie', 'Společenské vědy', 'Informatika']

app = Flask(__name__)
app.config['SECRET_KEY'] = '5e72ba27fc6a863eed13c27e6750bd25ab0be9ff55ac0e34823d966c1ce4896026992f2639857117'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app import routs