from threading import Thread
from flask_mail import Message
from app import app, mail
from flask import render_template

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
    sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template('email/' + template + '.txt', **kwargs)
    msg.html = render_template('email/' + template + '.html', **kwargs)
    mail.send(msg)