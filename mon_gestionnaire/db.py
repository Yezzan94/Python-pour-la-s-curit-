# Importation de la classe SQLAlchemy depuis l'extension flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# Création d'une instance globale de SQLAlchemy
# Cette instance sera utilisée pour toutes les interactions avec la base de données
db = SQLAlchemy()

# Définition d'une fonction pour initialiser la base de données
def init_db(app):
    # Initialisation de l'instance SQLAlchemy avec l'application Flask
    # Cela permet à SQLAlchemy de travailler avec la configuration et le contexte de l'application
    db.init_app(app)

    # Création d'un contexte d'application pour exécuter certaines tâches, comme la création de tables
    with app.app_context():
        # Création de toutes les tables définies dans les modèles
        # Les modèles doivent hériter de db.Model et être importés avant cet appel
        db.create_all()
