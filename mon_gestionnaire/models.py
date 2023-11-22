from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    # Ajoutez ici d'autres méthodes utiles pour le modèle User.

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [validators.EqualTo('password', message='Passwords must match')])
