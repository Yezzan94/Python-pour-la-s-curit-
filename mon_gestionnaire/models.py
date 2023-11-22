from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Ajoutez ici d'autres méthodes utiles pour le modèle User.

    def check_password(self, input_password):
        """Vérifie si le mot de passe correspond à celui de l'utilisateur."""
        return input_password == self.password

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])



class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    confirmpassword = PasswordField('Confirm Password', [validators.EqualTo('password', message='Passwords must match')])
