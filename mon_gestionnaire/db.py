from flask_sqlalchemy import SQLAlchemy
import hashlib
from cryptography.fernet import Fernet
from sqlalchemy_utils import URLType

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String)  # Clé de chiffrement pour les mots de passe

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hashed_password = self.hash_password(password)
        self.key = Fernet.generate_key().decode()

    @staticmethod
    def hash_password(password):
        """ Hash un mot de passe en utilisant SHA-256. """
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, input_password):
        """ Vérifie si le mot de passe fourni correspond au mot de passe haché. """
        return self.hash_password(input_password) == self.hashed_password

class StoredPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    site_name = db.Column(db.String(255), nullable=False)
    site_url = db.Column(URLType, nullable=True)  # Utilisation de URLType pour la validation des URL
    site_username = db.Column(db.String(80), nullable=False)
    secured_password = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    # user = db.relationship('User', backref='stored_passwords')  # Si nécessaire pour une relation réciproque

    def encrypt_password(self, plain_password):
        """ Chiffre le mot de passe avant de le stocker. """
        f = Fernet(self.user.key.encode())
        return f.encrypt(plain_password.encode()).decode()

    def decrypt_password(self):
        """ Déchiffre le mot de passe pour l'utilisation. """
        f = Fernet(self.user.key.encode())
        return f.decrypt(self.secured_password.encode()).decode()
