# Importation des modules nécessaires pour la création d'une application Flask
from flask import Flask, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Importation du module auth qui contient les routes d'authentification
from auth import auth

# Création de l'application Flask
app = Flask(__name__)

# Configuration de la clé secrète de l'application, nécessaire pour la session et les tokens CSRF
app.secret_key = 'une_clé_secrète_ici'
app.config['SECRET_KEY'] = 'une_autre_clé_secrète'

# Configuration de l'URI de la base de données pour SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)

# Initialisation de l'extension Flask-Migrate
migrate = Migrate(app, db)

# Importez les blueprints après l'initialisation de l'application
# Enregistrement du Blueprint 'auth' avec l'application Flask
# Cela ajoute les routes définies dans le module 'auth' à l'application
app.register_blueprint(auth)

# Définition de la route de la page d'accueil
@app.route('/')
def index():
    # Si l'utilisateur est connecté, redirige vers le tableau de bord
    if 'username' in session:
        return redirect(url_for('dashboard'))
    # Sinon, redirige vers la page de connexion
    return redirect(url_for('auth.login'))

# Définition de la route du tableau de bord
@app.route('/dashboard')
def dashboard():
    # Vérifie si l'utilisateur est connecté, sinon redirige vers la page de connexion
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    # Si connecté, affiche la page du tableau de bord
    return render_template('dashboard.html')  # Le template dashboard.html doit exister dans le dossier templates

# Point d'entrée principal pour exécuter l'application Flask
if __name__ == '__main__':
    # Création des tables de base de données dans un contexte d'application
    with app.app_context():
        db.create_all()

    # Lancement de l'application Flask en mode debug
    app.run(debug=True)

