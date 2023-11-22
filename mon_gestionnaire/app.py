from flask import Flask, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
import db
import auth

app = Flask(__name__)
app.secret_key = 'une_clé_secrète_ici'
app.config['SECRET_KEY'] = 'une_autre_clé_secrète'

csrf = CSRFProtect(app)
app.register_blueprint(auth.auth)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))  # Assurez-vous que cette route existe
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')  # Assurez-vous que ce template existe

if __name__ == '__main__':
    with app.app_context():
        db.init_db()
    app.run(debug=True)
