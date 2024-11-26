from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#user table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(20))
    #link every user to all the notes they create
    notes = db.relationship('Note')

#note table
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #relationship with user table 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
