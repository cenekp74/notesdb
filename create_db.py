from app import db 
from app.db_classes import User, Item
from app import app

with app.app_context():
    db.create_all()