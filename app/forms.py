# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

# Je définis le formulaire de connexion
class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

# Je définis le formulaire de création/modification de concert
class ConcertForm(FlaskForm):
    titre = StringField("Titre", validators=[DataRequired(), Length(max=200)])
    lieu = StringField("Lieu", validators=[DataRequired(), Length(max=200)])
    date = DateTimeLocalField("Date", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    nb_places_total = IntegerField("Nombre de places", validators=[DataRequired(), NumberRange(min=1)])
    categorie_id = SelectField("Catégorie", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

# Je définis le formulaire de création/modification d'actualité
class ActualiteForm(FlaskForm):
    titre = StringField("Titre", validators=[DataRequired(), Length(max=200)])
    contenu = TextAreaField("Contenu", validators=[DataRequired()])
    categorie_id = SelectField("Catégorie", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

# Je définis le formulaire de réservation de places
class ReservationForm(FlaskForm):
    nb_places = IntegerField("Nombre de places", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Réserver")

# Je définis le formulaire de commentaire sur un concert
class CommentaireForm(FlaskForm):
    auteur = StringField("Votre nom", validators=[DataRequired(), Length(max=100)])
    contenu = TextAreaField("Commentaire", validators=[DataRequired()])
    submit = SubmitField("Envoyer")
