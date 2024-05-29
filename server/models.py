# server/models.py
from __init__ import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(100), nullable=False, unique=True)

    def get_info(self):
        return {"tracking_number": self.tracking_number}

class TransitEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_detail = db.Column(db.String(255))
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))
