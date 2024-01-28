from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

VALID_ITEM_TYPES = ['zápisky', 'učebnice', 'prezentace', 'jiné']
VALID_SUBJECTS = ['', 'český jazyk a literatura', 'matematika', 'biologie', 'geografie (zeměpis)', 'dějepis', 'anglický jazyk', 'francouzský jazyk', 'německý jazyk', 'fyzika', 'chemie', 'společenské vědy', 'informatika', 'hudební výchova', 'výtvarná výchova']

app = Flask(__name__)
app.config['SECRET_KEY'] = '5e72ba27fc6a863eed13c27e6750bd25ab0be9ff55ac0e34823d966c1ce4896026992f2639857117'
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_SENDER'] = 'notesdb.cz@gmail.com'
app.config['MAIL_SUBJECT_PREFIX'] = 'NotesDB '

from flask_mail import Mail
mail = Mail(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)

from app import routs