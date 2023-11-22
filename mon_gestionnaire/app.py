from flask import Flask, render_template, request, redirect, url_for, flash, session
import password_manager_backend as backend

app = Flask(__name__)
app.secret_key = 'une_clé_secrète_ici'

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cipher_suite, error = backend.validate_login(username, password)
    if cipher_suite:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        flash(error or "Nom d'utilisateur ou mot de passe incorrect.")
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, error = backend.register_user(username, password)
        if success:
            flash("Inscription réussie. Veuillez vous connecter.")
            return redirect(url_for('index'))
        else:
            flash(error or "Une erreur est survenue lors de l'inscription.")
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Veuillez vous connecter pour accéder au tableau de bord.")
        return redirect(url_for('index'))
    # Ajouter ici la logique pour afficher les informations de l'utilisateur
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
