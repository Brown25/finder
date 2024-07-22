# server/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=150)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=150)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=150)])
    submit = SubmitField('Register')
    

class CreateLabelForm(FlaskForm):
    sender = StringField('Sender', validators=[InputRequired(), Length(min=4, max=150)])
    recipient = StringField('Recipient', validators=[InputRequired(), Length(min=4, max=150)])
    address = StringField('Address', validators=[InputRequired(), Length(min=4, max=255)])
    submit = SubmitField('Create Label')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')
