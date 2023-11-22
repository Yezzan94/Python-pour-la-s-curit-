from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
import password_manager_backend as backend
from models import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('.dashboard'))  # Assurez-vous que cette route existe

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Implémentez la logique de connexion dans backend
        cipher_suite, error = backend.login(username, password)
        if cipher_suite:
            session['username'] = username
            return redirect(url_for('.dashboard'))  # Assurez-vous que cette route existe
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
        return redirect(url_for('.dashboard'))  # Assurez-vous que cette route existe

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Implémentez la logique d'inscription dans backend
        success, error = backend.register_user(username, password)

        if success:
            flash("Inscription réussie. Veuillez vous connecter.")
            return redirect(url_for('.login'))
        else:
            flash(error or "Une erreur est survenue lors de l'inscription.")

    return render_template('register.html', form=form)
