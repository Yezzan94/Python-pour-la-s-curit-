import sqlite3
import hashlib
from cryptography.fernet import Fernet

def create_connection(db_file):
    """ Établit une connexion à la base de données SQLite spécifiée par db_file. """
    try:
        conn = sqlite3.connect(db_file)
        return conn, None
    except sqlite3.Error as error:
        return None, str(error)

def setup_database(conn):
    """ Crée les tables nécessaires dans la base de données si elles n'existent pas déjà. """
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (username text PRIMARY KEY, password_hash text, key text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS passwords (username text, service text, password text)''')
        conn.commit()
        return True, None
    except sqlite3.Error as error:
        return False, str(error)

def hash_password(password):
    """ Retourne le hachage SHA-256 du mot de passe fourni. """
    return hashlib.sha256(password.encode()).hexdigest()

def register(conn, username, password):
    """ Enregistre un nouvel utilisateur avec son mot de passe haché et une clé de chiffrement. """
    try:
        key = Fernet.generate_key()
        password_hash = hash_password(password)
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password_hash, key))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "Nom d'utilisateur déjà pris."
    except sqlite3.Error as error:
        return False, str(error)

def login(conn, username, password):
    """ Vérifie les identifiants de l'utilisateur et retourne un objet Fernet si la connexion réussit. """
    try:
        c = conn.cursor()
        c.execute("SELECT password_hash, key FROM users WHERE username=?", (username,))
        user = c.fetchone()
        if user and user[0] == hash_password(password):
            return Fernet(user[1]), None
        return None, "Nom d'utilisateur ou mot de passe incorrect."
    except sqlite3.Error as error:
        return None, str(error)

def add_password(conn, cipher_suite, username, service, password):
    """ Ajoute un mot de passe chiffré pour un utilisateur et un service spécifiques. """
    try:
        encrypted_password = cipher_suite.encrypt(password.encode())
        c = conn.cursor()
        c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (username, service, encrypted_password))
        conn.commit()
        return True, None
    except sqlite3.Error as error:
        return False, str(error)

def get_password(conn, cipher_suite, username, service):
    """ Récupère et déchiffre le mot de passe d'un utilisateur pour un service spécifique. """
    try:
        c = conn.cursor()
        c.execute("SELECT password FROM passwords WHERE username=? AND service=?", (username, service))
        result = c.fetchone()
        if result:
            decrypted_password = cipher_suite.decrypt(result[0]).decode()
            return decrypted_password, None
        return None, "Service non trouvé."
    except sqlite3.Error as error:
        return None, str(error)
