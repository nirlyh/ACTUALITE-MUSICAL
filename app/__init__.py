# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

# Je crée mes extensions en global pour pouvoir les utiliser dans tout le projet
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    # Je crée mon instance de l'application Flask
    app = Flask(__name__)

    # Je configure ma clé secrète pour les formulaires Flask-WTF
    app.config['SECRET_KEY'] = 'change-moi-en-vrai-secret'

    # Je configure la connexion à ma base MariaDB
    # À adapter avec tes vrais identifiants
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/actualite_musicale'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # J'initialise les extensions avec mon app
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Je définis la vue de login par défaut pour Flask-Login
    login_manager.login_view = 'main.login'

    # J'importe les routes après la création de l'app pour éviter les imports circulaires
    from app import routes
    app.register_blueprint(routes.main_bp)

    # Je retourne l'application configurée
    from app import models
    return app
