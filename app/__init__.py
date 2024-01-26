from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

VALID_ITEM_TYPES = ['zápisky', 'učebnice', 'prezentace', 'jiné']
VALID_SUBJECTS = ['', 'český jazyk a literatura', 'matematika', 'biologie', 'geografie (zeměpis)', 'dějepis', 'anglický jazyk', 'francouzský jazyk', 'německý jazyk', 'fyzika', 'chemie', 'společenské vědy', 'informatika']

app = Flask(__name__)
app.config['SECRET_KEY'] = '5e72ba27fc6a863eed13c27e6750bd25ab0be9ff55ac0e34823d966c1ce4896026992f2639857117'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app import routs