# src/models.py

from database import Database

db = Database().db

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(20), unique=True, nullable=False)
    tracking_url = db.Column(db.String(120), nullable=False)
    support_phone_numbers = db.Column(db.String(120), nullable=False)
    create_date = db.Column(db.String(120), nullable=True)
    promised_date = db.Column(db.String(120), nullable=True)
    transit_events = db.relationship('TransitEvent', backref='package', lazy=True)

class TransitEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
