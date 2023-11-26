#Importation des modules nécessaires
import logging
from flask import Flask, render_template, request, session, redirect
from flask_mongoengine import MongoEngine
from flask_session import Session
from modules.PasswordGenerator import PasswordGenerator
from passlib.hash import pbkdf2_sha256
from datetime import timedelta

logging.basicConfig(filename='app.log', level=logging.INFO)

#Initialisation de l'app Flask
app = Flask(
    __name__,
    static_url_path='',
    static_folder='mon_gestionnaire/static',
    template_folder='mon_gestionnaire/templates',
)

# Configuration des sessions et de la base de données
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MONGODB_SETTINGS'] = {
    'db': 'password_manager',
    'host': 'localhost',
    'port': 27017
}
Session(app)
db = MongoEngine(app)

# Définition des modèles de données
class NewUser(db.Document):
    name = db.StringField()
    email = db.StringField()
    username = db.StringField()
    password = db.StringField()
    failed_login_attempts = db.IntField(default=0)
    last_failed_login = db.DateTimeField()


    def to_json(self):
        # Méthode pour convertir un utilisateur en JSON
        return {
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'password': self.password,
        }


class Passwords(db.Document):
    #Champs pour le modèle password
    user = db.StringField()
    website = db.StringField()
    username = db.StringField()
    password = db.StringField()

    def to_json(self):
        return {
            "website": self.website,
            "username": self.username,
            "password": self.password,
        }



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html', error_message='')


@app.route('/login.py', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        username = request.form['login--username']
        password = request.form['login--password']
        user = NewUser.objects(username=username).first()

        if user:
            if user and user.failed_login_attempts >= 3:
        # Vérifier si suffisamment de temps s'est écoulé
                if user.last_failed_login and datetime.utcnow() - user.last_failed_login > timedelta(minutes=1):
                    user.failed_login_attempts = 0  # Réinitialiser le compteur
                else:
                    return render_template('login.html', error_message="Compte bloqué après 3 tentatives erronées")

            if pbkdf2_sha256.verify(password, user.password):
                user.failed_login_attempts = 0
                user.save()
                session['username'] = user.username
                session.permanent = True
                return render_template('/main.html', user=user.name, username=user.username)
            else:
                user.failed_login_attempts += 1
                user.save()
                logging.warning(f"Tentative de connexion échouée pour {username}")
        
        return render_template('login.html', error_message="Nom d'utilisateur ou Mot de passe incorrect")
    else:
        return render_template('login.html', error_message='')



@app.route('/register')
def register():
    return render_template('register.html', error_message='')



@app.route('/register.py', methods=['POST'])
def register_user():
    username = request.form['register--username']
    user = NewUser.objects(username=username).first()
    if user:
        return render_template("register.html", error_message="Le nom d'utilisateur est déjà pris")
    else:
        password = request.form['register--password']
        hashed_password = pbkdf2_sha256.hash(password)
        new_user = NewUser(
            name=request.form['register--name'],
            email=request.form['register--email'],
            username=username,
            password=hashed_password
        )
        new_user.save()
        return render_template('login.html')



@app.route('/gen_pass')
def generate_password():
    PSWD = PasswordGenerator()
    return {"password": f'{PSWD.get_password()}'}


@app.route('/save_pass', methods=['POST','GET'])
def save_password():
    # Handle Same username for same website
    data = request.get_json()
    password = Passwords.objects(
        user=session['username'], website=data['website'], username=data['username']).first()
    if password:
        return {"message": "Exists"}
    new_pass = Passwords(
        user=data['user'],
        website=data['website'],
        username=data['username'],
        password=data['password'],
    )
    new_pass.save()
    return {'message': 'Saved'}, 200


@app.route('/get_pass', methods=['GET'])
def get_password():
    if not session['username']:
        return redirect('/')
    passwords = Passwords.objects(user=session['username']).filter()
    data = []
    for password in passwords:
        password = password.to_json()
        data.append(password)
    return {"passwords": data}, 200


@app.route('/search_pass', methods=['POST'])
def search_password():
    if not session['username']:
        redirect('/')
    data = request.get_json()
    passwords = Passwords.objects(
        user=data['username'],
        website=data['website']
    ).filter()
    data = []
    for password in passwords:
        password.to_json()
        data.append(password)
    return {"passwords": data}, 200


@app.route('/del_pass', methods=['POST'])
def delete_password():
    if not session['username']:
        return redirect('/')
    data = request.get_json()
    password = Passwords.objects(
        user=session['username'],
        website=data['website'],
        username=data['username']
    ).first()
    password.delete()
    return {"message": "OK"}, 200


@app.route('/logout.py')
def logout():
    session['username'] = None
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
