import sqlite3
import hashlib
from cryptography.fernet import Fernet

def create_connection(db_file='votre_base_de_donnees.db'):
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as error:
        print(f"Erreur de connexion à la base de données: {error}")
        return None  # Retourne None en cas d'erreur
    return conn

def setup_database():
    conn = create_connection()
    try:
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users (username text PRIMARY KEY, password_hash text, key text)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS passwords (username text, service text, password text)''')
    finally:
        conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = create_connection()
    try:
        key = Fernet.generate_key()
        password_hash = hash_password(password)
        with conn:
            conn.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password_hash, key))
        return True, None
    except sqlite3.IntegrityError:
        return False, "Nom d'utilisateur déjà pris."
    finally:
        conn.close()


def login(username, password):
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT password_hash, key FROM users WHERE username=?", (username,))
        user = c.fetchone()
        if user and user[0] == hash_password(password):
            return Fernet(user[1]), None
        return None, "Nom d'utilisateur ou mot de passe incorrect."
    finally:
        conn.close()

def add_password(username, service, password):
    conn = create_connection()
    try:
        cipher_suite = Fernet(generate_user_key(username, conn))
        encrypted_password = cipher_suite.encrypt(password.encode())
        with conn:
            conn.execute("INSERT INTO passwords VALUES (?, ?, ?)", (username, service, encrypted_password))
        return True, None
    finally:
        conn.close()

def get_password(username, service):
    conn = create_connection()
    try:
        cipher_suite = Fernet(generate_user_key(username, conn))
        c = conn.cursor()
        c.execute("SELECT password FROM passwords WHERE username=? AND service=?", (username, service))
        result = c.fetchone()
        if result:
            decrypted_password = cipher_suite.decrypt(result[0]).decode()
            return decrypted_password, None
        return None, "Service non trouvé."
    finally:
        conn.close()

def generate_user_key(username, conn):
    c = conn.cursor()
    c.execute("SELECT key FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        return result[0]
    raise Exception("User key not found.")
