from db import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
import hashlib
from cryptography.fernet import Fernet

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    key = db.Column(db.String)  # Clé de chiffrement pour les mots de passe

    def __init__(self, username, password):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.key = Fernet.generate_key().decode()  # Génère une clé de chiffrement unique

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, input_password):
        return self.hash_password(input_password) == self.password_hash

class StoredPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', backref='stored_passwords')

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    confirmpassword = PasswordField('Confirm Password', [validators.EqualTo('password', message='Passwords must match')])
