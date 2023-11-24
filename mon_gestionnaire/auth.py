# Importations nécessaires pour la création de routes et l'affichage de templates dans Flask
from flask import Blueprint, render_template, redirect, url_for, flash, session
# Importation de FlaskForm pour la gestion des formulaires
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
# Importation du modèle User et de l'instance db pour les interactions avec la base de données


auth = Blueprint('auth', __name__)

# Définition de la route pour la connexion
@auth.route('/login', methods=['GET', 'POST'])
def login():
    from models import LoginForm
    from db import User

    # Vérifier si l'utilisateur est déjà connecté
    if 'username' in session:
        # Rediriger vers la page du tableau de bord si déjà connecté
        return redirect(url_for('dashboard'))

    # Création d'une instance du formulaire de connexion
    form = LoginForm()

    # Vérification de la validité du formulaire après soumission
    if form.validate_on_submit():
        # Récupération des données du formulaire
        username = form.username.data
        password = form.password.data

        # Recherche de l'utilisateur dans la base de données
        user = User.query.filter_by(username=username).first()

        # Vérification si l'utilisateur existe et si le mot de passe est correct
        if user and user.check_password(password):
            # Si authentification réussie, enregistrer le nom d'utilisateur dans la session
            session['username'] = username
            # Redirection vers le tableau de bord
            return redirect(url_for('dashboard'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            flash("Nom d'utilisateur ou mot de passe incorrect.")

    # Afficher le formulaire de connexion
    return render_template('login.html', form=form)


# Définition de la route pour la déconnexion
@auth.route('/logout')
def logout():
    # Supprimer le nom d'utilisateur de la session
    session.pop('username', None)
    # Rediriger vers la page de connexion
    return redirect(url_for('.login'))

# Définition de la route pour l'inscription
@auth.route('/register', methods=['GET', 'POST'])
def register():
    from models import RegisterForm
    from db import User, db
    # Si l'utilisateur est déjà connecté, rediriger vers le tableau de bord
    if 'username' in session:
        return redirect(url_for('dashboard'))


    # Création d'une instance du formulaire d'inscription
    form = RegisterForm()
    # Traitement du formulaire après soumission
    if form.validate_on_submit():
        # Récupération des données du formulaire
        username = form.username.data
        email = form.email.data  # Email n'est pas utilisé dans ce bloc mais pourrait être utilisé dans une version future
        password = form.password.data

        # Vérification si l'utilisateur existe déjà dans la base de données
        user = User.query.filter_by(username=username).first()
        if user:
            # Si l'utilisateur existe déjà, afficher un message d'erreur
            flash("Nom d'utilisateur déjà pris.")
            return render_template('register.html', form=form)

        try:
            # Création d'un nouvel utilisateur et ajout à la base de données
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()  # Tentative de valider les modifications

            # Si aucune exception n'est levée, flasher un message de succès
            flash("Inscription réussie. Veuillez vous connecter.")
            return redirect(url_for('.login'))  # Redirection vers la page de connexion
        except Exception as e:
            # Si une exception est levée, flasher un message d'erreur
            flash("Une erreur est survenue lors de l'inscription.")
            db.session.rollback()  # Annuler les modifications en cas d'erreur

    # Afficher le formulaire d'inscription si aucune soumission valide n'a eu lieu
    return render_template('register.html', form=form)
