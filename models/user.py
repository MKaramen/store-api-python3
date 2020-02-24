import sqlite3
from db import db


class UserModel(db.Model):
    # * SQL-ALCHEMY - The properties name of the class and the properties of Alchemy must have the same name otherwiste they wont be saved to the db
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # ? 16 => is the limit of character
    username = db.Column(db.String(16))
    password = db.Column(db.String(16))
    # *

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
