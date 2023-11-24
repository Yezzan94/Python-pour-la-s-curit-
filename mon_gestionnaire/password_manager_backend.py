from models import db
from db import User, StoredPassword
import hashlib
from cryptography.fernet import Fernet

def hash_password(password):
    """ Retourne le hachage SHA-256 du mot de passe fourni. """
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """ Enregistre un nouvel utilisateur avec son mot de passe haché et une clé de chiffrement. """
    try:
        key = Fernet.generate_key().decode()  # Générer et décoder la clé de chiffrement
        password_hash = hash_password(password)
        new_user = User(username=username, password_hash=password_hash, key=key)
        db.session.add(new_user)
        db.session.commit()
        return True, None
    except Exception as error:
        db.session.rollback()
        return False, str(error)

def login(username, password):
    """ Vérifie les identifiants de l'utilisateur et retourne un objet Fernet si la connexion réussit. """
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return Fernet(user.key.encode()), None  # Encodez la clé avant de l'utiliser
    return None, "Nom d'utilisateur ou mot de passe incorrect."

def add_password(user_id, service, username, password):
    """ Ajoute un mot de passe chiffré pour un utilisateur et un service spécifiques. """
    user = User.query.get(user_id)
    if user:
        cipher_suite = Fernet(user.key.encode())  # Encodez la clé avant de l'utiliser
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()
        new_password = StoredPassword(user_id=user_id, service=service, username=username, encrypted_password=encrypted_password)
        db.session.add(new_password)
        db.session.commit()
        return True, "Mot de passe ajouté avec succès."
    return False, "Utilisateur non trouvé."

def get_password(user_id, service):
    """ Récupère et déchiffre le mot de passe d'un utilisateur pour un service spécifique. """
    user = User.query.get(user_id)
    if user:
        cipher_suite = Fernet(user.key.encode())  # Encodez la clé avant de l'utiliser
        stored_password = StoredPassword.query.filter_by(user_id=user_id, service=service).first()
        if stored_password:
            decrypted_password = cipher_suite.decrypt(stored_password.encrypted_password.encode()).decode()
            return decrypted_password, "Mot de passe récupéré avec succès."
    return None, "Mot de passe non trouvé ou utilisateur non existant."
