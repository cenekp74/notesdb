import secrets
from app.db_classes import Item

def generate_unique_folder_hex():
    while True:
        folder = secrets.token_hex(3)
        if not Item.query.filter_by(folder=folder).first():
            return folder
