from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize, MultipleFileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TimeField, IntegerField, ValidationError, SelectField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange, Email, Length, EqualTo
from app.db_classes import User
from flask_login import current_user
from app import VALID_ITEM_TYPES, VALID_SUBJECTS

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "email"})
    password = PasswordField('Heslo', validators=[DataRequired()], render_kw={"placeholder": "heslo"})
    remember = BooleanField('Pamatuj si mě')
    submit = SubmitField('Přihlásit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "uživatelské jméno"})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=120)], render_kw={"placeholder": "email"})
    password = PasswordField('Heslo', validators=[DataRequired()], render_kw={"placeholder": "heslo"})
    confirm_password = PasswordField('Potvrdit heslo', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "heslo znovu"})
    submit = SubmitField('Registrovat')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Uživatelské jméno je již zabrané')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email je již používán')
        
class UpdateaccForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Jméno', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=120)])
    pp = FileField('Profilový obrázek', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Uložit')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Uživatelské jméno je již zabrané')
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email je již používán')
            
class ItemForm(FlaskForm):
    name = StringField('Název', validators=[DataRequired(), Length(min=4, max=30)])
    files = MultipleFileField('Soubory', validators=[FileRequired(), FileSize(max_size=30000000)])
    item_type = SelectField('Typ', choices=VALID_ITEM_TYPES, validators=[DataRequired()])
    author = StringField('Autor', validators=[Length(min=2, max=100)])
    tags = StringField('Tagy (oddělené mezerou)', validators=[Length(max=200)])
    prof = StringField('Profesor', validators=[Length(max=100)])
    note = TextAreaField('Poznámky')
    subject = SelectField('Předmět', choices=VALID_SUBJECTS)
    submit = SubmitField('Potvrdit')