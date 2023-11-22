from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
import password_manager_backend as backend  # Assurez-vous que le chemin d'importation est correct
from models import *
from db import *  # Assurez-vous que vous importez la connexion à la base de données


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Rechercher l'utilisateur par nom d'utilisateur
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Le mot de passe correspond, connectez l'utilisateur
            session['username'] = username
            return redirect(url_for('template/dashboard'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.")

    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('template/dashboard'))  # Assurez-vous que cette route existe

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data  # Récupérez l'e-mail du formulaire
        password = form.password.data
        # Implémentez la logique d'inscription dans backend
        success, error = backend.register_user(conn, username, email, password)  # Passez la connexion en premier argument

        if success:
            flash("Inscription réussie. Veuillez vous connecter.")
            return redirect(url_for('auth.login'))
        else:
            flash(error or "Une erreur est survenue lors de l'inscription.")

    return render_template('register.html', form=form)
