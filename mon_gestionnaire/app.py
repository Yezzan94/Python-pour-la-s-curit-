import os
from flask import Flask, redirect, url_for, session, render_template
from db import db, User
from flask_migrate import Migrate
import subprocess  # Ajout de l'importation du module subprocess

def create_app():

    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')

    app = Flask(__name__)

    # Configuration de l'application
    app.config['SECRET_KEY'] = 'une_clé_secrète_ici'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'my_database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialisation de l'instance SQLAlchemy avec l'application Flask
    db.init_app(app)

    # Initialisation de Flask-Migrate
    migrate = Migrate(app, db)

    # Enregistrement du Blueprint 'auth' avec l'application Flask (à adapter selon votre configuration)
    from auth import auth
    app.register_blueprint(auth)

    # Définition des routes
    @app.route('/')
    def index():
        if 'username' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('auth.login'))

    @app.route('/dashboard')
    def dashboard():
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return render_template('dashboard.html')

    # Fonction pour exécuter les migrations
    def run_migrations():
        try:
            # Exécutez les commandes de migration
            subprocess.run(["flask", "db", "init"])
            subprocess.run(["flask", "db", "migrate"])
            subprocess.run(["flask", "db", "upgrade"])
            print("Migrations successfully applied.")
        except Exception as e:
            print(f"Error applying migrations: {str(e)}")

    # Appel de la fonction pour exécuter les migrations au démarrage de l'application
    run_migrations()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
