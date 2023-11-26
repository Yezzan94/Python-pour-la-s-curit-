# suppr_db.py

from app import NewUser  # Assurez-vous que ce chemin d'importation est correct
from mongoengine import connect

# Connexion à la base de données MongoDB
connect('password_manager', host='localhost', port=27017)

# Suppression de tous les utilisateurs
NewUser.objects.delete()

print("Tous les utilisateurs ont été supprimés.")

