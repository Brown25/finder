# src/database.py

from flask_sqlalchemy import SQLAlchemy

class Database:
    def __init__(self, app=None):
        self.db = SQLAlchemy(app)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.db.init_app(app)
        with app.app_context():
            self.db.create_all()
