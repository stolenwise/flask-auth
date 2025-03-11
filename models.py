from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import db


class User(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    
    def __repr__(self):
        return f'<User {self.username}>'