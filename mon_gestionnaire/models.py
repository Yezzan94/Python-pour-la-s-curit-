from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(message="Username is required")])
    password = PasswordField('Password', [validators.DataRequired(message="Password is required")])

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(message="Username is required")])
    email = StringField('Email', [validators.DataRequired(message="Email is required"), validators.Email(message="Invalid email format")])
    password = PasswordField('Password', [validators.DataRequired(message="Password is required")])
    confirmpassword = PasswordField('Confirm Password', [
        validators.EqualTo('password', message='Passwords must match'),
        validators.DataRequired(message="Please confirm your password")
    ])
