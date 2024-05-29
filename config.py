# config.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configuration
# Use the absolute path to the database file
basedir = os.path.abspath(os.path.dirname(__file__))  # Get the directory of config.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'my_app.db')  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to avoid warnings

# Initialize the SQLAlchemy database object
db = SQLAlchemy(app)

# Create the database and tables (optional, but useful during development)
with app.app_context():
    db.create_all()
