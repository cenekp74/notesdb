from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TimeField, IntegerField, ValidationError, SelectField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange, Email, Length, EqualTo
from app.db_classes import User


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