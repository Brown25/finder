from __init__ import create_app, db, login_manager, bcrypt  # Ensure bcrypt is imported from __init__.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Package
from forms import LoginForm, RegisterForm  # Assuming you have these forms defined in forms.py
from datetime import datetime

from datetime import datetime

class Label:
    def __init__(self, tracking_number, sender, recipient, address):
        self.tracking_number = tracking_number
        self.sender = sender
        self.recipient = recipient
        self.address = address
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_label_info(self):
        return {
            "tracking_number": self.tracking_number,
            "sender": self.sender,
            "recipient": self.recipient,
            "address": self.address,
            "creation_date": self.creation_date
        }
