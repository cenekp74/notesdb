from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

VALID_ITEM_TYPES = ['zápisky', 'učebnice', 'prezentace', 'jiné']
VALID_SUBJECTS = ['', 'český jazyk a literatura', 'matematika', 'biologie', 'geografie (zeměpis)', 'dějepis', 'anglický jazyk', 'francouzský jazyk', 'německý jazyk', 'fyzika', 'chemie', 'společenské vědy', 'informatika', 'hudební výchova', 'výtvarná výchova']
VALID_PROFESSORS =  ['', 'Karel Bednář', 'Kateřina Borovičková', 'Karel Bříza', 'Kateřina Burgetová', 'Christopher Dunn', 'Natálie Dunn', 'Filip Dušek', 'Blanka Fabriková', 'Jakub Fajfr', 'Anke Fillibeck', 'Gabriela Gaudlová', 'Eva Chmelařová', 'Karel Chottous', 'Lenka Janečková', 'Zuzana Korcová', 'Nathalie Lamandé', 'Martin Mejzr', 'Jana Moravcová', 'Marie Nosková', 'Kateřina Odcházelová', 'Blanka Pešková', 'Jaroslav Picka', 'Ina Rajsiglová', 'Roman Sixta', 'Martina Skuhravá', 'Michal Slačík', 'Markéta Smetanová', 'David Staněk', 'Kristýna Svobodová', 'Jiří Šlédr', 'Jana Škvorová', 'Jan Šperling', 'Martin Švejnoha', 'Jaromír Tkadleček', 'Jana Tláskalová', 'Michala Tomková', 'Jana Třeštíková', 'Josef Tvrský', 'Alena Volfová', 'Nela Žižková']

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
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