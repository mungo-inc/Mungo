from flask_login import UserMixin
from .index import db

class Client(db.Model, UserMixin):
    __tablename__ = 'client'

    id_client = db.Column(db.Integer, primary_key = True)
    courriel = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text,  nullable=False)

    def __init__(self, courriel, password):
        self.courriel = courriel
        self.password = password

    def get_id(self):
        return self.id_client
