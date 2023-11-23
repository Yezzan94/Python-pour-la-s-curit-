# Importation de l'instance db depuis le fichier db.py pour l'utilisation de SQLAlchemy
from db import db
# Importations nécessaires pour créer des formulaires avec Flask-WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
# Importation de la bibliothèque hashlib pour le hachage des mots de passe
import hashlib

# Définition du modèle User pour représenter les utilisateurs dans la base de données
class User(db.Model):
    # Déclaration des colonnes de la table des utilisateurs
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique pour chaque utilisateur
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nom d'utilisateur, unique et requis
    password_hash = db.Column(db.String(120), nullable=False)  # Hachage du mot de passe, requis

    # Constructeur pour initialiser les instances de la classe User
    def __init__(self, username, password):
        self.username = username  # Attribue le nom d'utilisateur fourni
        self.password_hash = self.hash_password(password)  # Hachage du mot de passe fourni

    # Méthode statique pour hacher les mots de passe
    @staticmethod
    def hash_password(password):
        """ Retourne le hachage SHA-256 du mot de passe fourni. """
        return hashlib.sha256(password.encode()).hexdigest()

    # Méthode pour vérifier si un mot de passe fourni correspond au hachage stocké
    def check_password(self, input_password):
        """Vérifie si le mot de passe correspond à celui haché de l'utilisateur."""
        return self.hash_password(input_password) == self.password_hash

# Définition de la classe LoginForm pour le formulaire de connexion
class LoginForm(FlaskForm):
    # Champ de nom d'utilisateur, requis
    username = StringField('Username', [validators.DataRequired()])
    # Champ de mot de passe, requis
    password = PasswordField('Password', [validators.DataRequired()])

# Définition de la classe RegisterForm pour le formulaire d'inscription
class RegisterForm(FlaskForm):
    # Champ de nom d'utilisateur, requis
    username = StringField('Username', [validators.DataRequired()])
    # Champ d'email, requis
    email = StringField('Email', [validators.DataRequired()])
    # Champ de mot de passe, requis
    password = PasswordField('Password', [validators.DataRequired()])
    # Champ de confirmation de mot de passe, doit correspondre au champ de mot de passe
    confirmpassword = PasswordField('Confirm Password', [validators.EqualTo('password', message='Passwords must match')])
