# import_users.py

from app import NewUser
from mongoengine import connect

def read_all_users():
    # Connexion à la base de données
    connect('password_manager', host='localhost', port=27017)

    # Lecture et affichage de tous les utilisateurs
    users = NewUser.objects()
    for user in users:
        print(f"Nom: {user.name}, Email: {user.email}, Nom d'utilisateur: {user.username}")

if __name__ == "__main__":
    read_all_users()

