# Importation des modules nécessaires
from models import db, User  # Importation du modèle User et de l'instance de base de données
import hashlib  # Pour le hachage des mots de passe
from cryptography.fernet import Fernet  # Pour le chiffrement

def hash_password(password):
    """ Retourne le hachage SHA-256 du mot de passe fourni. """
    # Utilisation de hashlib pour créer un hachage SHA-256 du mot de passe
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """ Enregistre un nouvel utilisateur avec son mot de passe haché et une clé de chiffrement. """
    try:
        # Génération d'une clé de chiffrement unique pour chaque utilisateur
        key = Fernet.generate_key()
        # Hachage du mot de passe fourni
        password_hash = hash_password(password)
        # Création d'un nouvel utilisateur avec le nom d'utilisateur, le hachage du mot de passe et la clé de chiffrement
        new_user = User(username=username, password=password_hash)
        # Ajout du nouvel utilisateur à la session de base de données
        db.session.add(new_user)
        # Enregistrement des modifications dans la base de données
        db.session.commit()
        return True, None
    except Exception as error:
        # En cas d'erreur, annuler les modifications
        db.session.rollback()
        return False, str(error)

def login(username, password):
    """ Vérifie les identifiants de l'utilisateur et retourne un objet Fernet si la connexion réussit. """
    # Recherche de l'utilisateur par son nom d'utilisateur
    user = User.query.filter_by(username=username).first()
    # Vérification si l'utilisateur existe et si le mot de passe fourni correspond au hachage stocké
    if user and user.password == hash_password(password):
        # Retourne un objet Fernet pour le chiffrement/déchiffrement basé sur la clé de l'utilisateur
        return Fernet(user.key), None
    return None, "Nom d'utilisateur ou mot de passe incorrect."

def add_password(cipher_suite, username, service, password):
    """ Ajoute un mot de passe chiffré pour un utilisateur et un service spécifiques. """
    # Cette fonction doit être implémentée pour stocker les mots de passe chiffrés associés à un utilisateur et un service
    pass

def get_password(cipher_suite, username, service):
    """ Récupère et déchiffre le mot de passe d'un utilisateur pour un service spécifique. """
    # Cette fonction doit être implémentée pour récupérer et déchiffrer les mots de passe stockés
    pass
