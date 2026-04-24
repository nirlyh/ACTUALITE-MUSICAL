# app/models.py

from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login_manager

# Je définis mon modèle utilisateur pour gérer l'authentification
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Je définis le callback pour charger un utilisateur via Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Je définis la catégorie d'actualité (rock, pop, etc.)
class CategorieActualite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    actualites = db.relationship('Actualite', backref='categorie', lazy=True)

# Je définis la catégorie de concert (festival, salle, etc.)
class CategorieConcert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    concerts = db.relationship('Concert', backref='categorie', lazy=True)

# Je définis le modèle pour les concerts
class Concert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    lieu = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    nb_places_total = db.Column(db.Integer, nullable=False)
    nb_places_reservees = db.Column(db.Integer, default=0)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie_concert.id'), nullable=False)
    # Pour les concerts passés, je pourrai lier des commentaires, photos, etc.
    commentaires = db.relationship('Commentaire', backref='concert', lazy=True)

# Je définis le modèle pour les actualités musicales
class Actualite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie_actualite.id'), nullable=False)

# Je définis le modèle pour les commentaires sur les concerts
class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auteur = db.Column(db.String(100), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.id'), nullable=False)
