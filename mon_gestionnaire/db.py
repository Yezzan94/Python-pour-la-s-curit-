# Importation de la classe SQLAlchemy depuis l'extension flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Création de l'instance globale de SQLAlchemy
db = SQLAlchemy()

# Modèle pour la table "username"
class Username(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# Modèle pour la table "email"
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Modèle pour la table "password"
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)

# Modèle pour la table "account_info"
class AccountInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(255), nullable=False)
    site_url = db.Column(db.String(255), nullable=True)

# Configuration de la base de données
DATABASE_URI = 'sqlite:///my_database.db'

# Fonction pour initialiser la base de données
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
