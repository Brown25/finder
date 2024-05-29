# database.py

from flask_sqlalchemy import SQLAlchemy


# Create SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)
    # Create database tables
    with app.app_context():
        db.create_all()
