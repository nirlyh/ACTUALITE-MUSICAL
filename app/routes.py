# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta

from app import db
from app.models import Concert, Actualite, CategorieConcert, CategorieActualite, User, Commentaire
from app.forms import LoginForm, ConcertForm, ActualiteForm, ReservationForm, CommentaireForm

# Je crée un blueprint pour regrouper toutes mes routes
main_bp = Blueprint('main', __name__)

# Je définis la page d'accueil qui affiche les X dernières actualités et concerts à venir
@main_bp.route('/')
def index():
    # Je récupère les 5 dernières actualités
    actualites = Actualite.query.order_by(Actualite.date_publication.desc()).limit(5).all()
    # Je récupère les 5 prochains concerts
    concerts = Concert.query.filter(Concert.date >= datetime.utcnow()).order_by(Concert.date.asc()).limit(5).all()
    return render_template('index.html', actualites=actualites, concerts=concerts)

# Je définis la page listant les concerts avec filtres
@main_bp.route('/concerts')
def concerts():
    type_id = request.args.get('type', type=int)
    lieu = request.args.get('lieu', type=str)
    date_str = request.args.get('date', type=str)

    query = Concert.query

    # Je filtre par catégorie si un type est fourni
    if type_id:
        query = query.filter_by(categorie_id=type_id)

    # Je filtre par lieu si un lieu est fourni
    if lieu:
        query = query.filter(Concert.lieu.ilike(f"%{lieu}%"))

    # Je filtre par date si une date est fournie
    if date_str:
        try:
            date_filtre = datetime.strptime(date_str, "%Y-%m-%d")
            query = query.filter(db.func.date(Concert.date) == date_filtre.date())
        except ValueError:
            flash("Format de date invalide. Utiliser AAAA-MM-JJ.", "danger")

    concerts = query.order_by(Concert.date.asc()).all()
    categories = CategorieConcert.query.all()

    return render_template('concerts/liste.html', concerts=concerts, categories=categories)

# Je définis la page détail d'un concert avec réservation et commentaires
@main_bp.route('/concerts/<int:concert_id>', methods=['GET', 'POST'])
def concert_detail(concert_id):
    concert = Concert.query.get_or_404(concert_id)
    reservation_form = ReservationForm()
    commentaire_form = CommentaireForm()

    # Je gère la réservation de places
    if reservation_form.validate_on_submit() and 'reserver' in request.form:
        nb_places = reservation_form.nb_places.data
        places_disponibles = concert.nb_places_total - concert.nb_places_reservees

        if nb_places <= places_disponibles:
            concert.nb_places_reservees += nb_places
            db.session.commit()
            flash("Réservation effectuée avec succès.", "success")
        else:
            flash("Pas assez de places disponibles.", "danger")

        return redirect(url_for('main.concert_detail', concert_id=concert.id))

    # Je gère l'ajout d'un commentaire
    if commentaire_form.validate_on_submit() and 'commenter' in request.form:
        commentaire = Commentaire(
            auteur=commentaire_form.auteur.data,
            contenu=commentaire_form.contenu.data,
            concert=concert
        )
        db.session.add(commentaire)
        db.session.commit()
        flash("Commentaire ajouté.", "success")
        return redirect(url_for('main.concert_detail', concert_id=concert.id))

    # Je calcule si je dois afficher la météo (concert dans les 15 jours)
    afficher_meteo = False
    if 0 <= (concert.date - datetime.utcnow()).days <= 15:
        afficher_meteo = True
        # Ici je pourrais appeler une API météo si c'était autorisé

    return render_template(
        'concerts/detail.html',
        concert=concert,
        reservation_form=reservation_form,
        commentaire_form=commentaire_form,
        afficher_meteo=afficher_meteo
    )

# Je définis la page listant les actualités par catégorie
@main_bp.route('/actualites')
def actualites():
    categorie_id = request.args.get('categorie', type=int)
    query = Actualite.query

    if categorie_id:
        query = query.filter_by(categorie_id=categorie_id)

    actualites = query.order_by(Actualite.date_publication.desc()).all()
    categories = CategorieActualite.query.all()

    return render_template('actualites/liste.html', actualites=actualites, categories=categories)

# Je définis la page de login pour l'administration
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Ici je devrais vérifier le hash du mot de passe
        if user:
            login_user(user)
            flash("Connexion réussie.", "success")
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash("Identifiants invalides.", "danger")
    return render_template('auth/login.html', form=form)

# Je définis la route de déconnexion
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('main.index'))

# Je définis le tableau de bord d'administration
@main_bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Accès refusé.", "danger")
        return redirect(url_for('main.index'))
    return render_template('admin/dashboard.html')

# Je définis la gestion des concerts en administration
@main_bp.route('/admin/concerts', methods=['GET', 'POST'])
@login_required
def admin_concerts():
    if not current_user.is_admin:
        flash("Accès refusé.", "danger")
        return redirect(url_for('main.index'))

    form = ConcertForm()
    form.categorie_id.choices = [(c.id, c.nom) for c in CategorieConcert.query.all()]

    if form.validate_on_submit():
        concert = Concert(
            titre=form.titre.data,
            lieu=form.lieu.data,
            date=form.date.data,
            nb_places_total=form.nb_places_total.data,
            categorie_id=form.categorie_id.data
        )
        db.session.add(concert)
        db.session.commit()
        flash("Concert ajouté.", "success")
        return redirect(url_for('main.admin_concerts'))

    concerts = Concert.query.order_by(Concert.date.desc()).all()
    return render_template('concerts/admin_concerts.html', form=form, concerts=concerts)

# Je définis la gestion des actualités en administration
@main_bp.route('/admin/actualites', methods=['GET', 'POST'])
@login_required
def admin_actualites():
    if not current_user.is_admin:
        flash("Accès refusé.", "danger")
        return redirect(url_for('main.index'))

    form = ActualiteForm()
    form.categorie_id.choices = [(c.id, c.nom) for c in CategorieActualite.query.all()]

    if form.validate_on_submit():
        actualite = Actualite(
            titre=form.titre.data,
            contenu=form.contenu.data,
            categorie_id=form.categorie_id.data
        )
        db.session.add(actualite)
        db.session.commit()
        flash("Actualité ajoutée.", "success")
        return redirect(url_for('main.admin_actualites'))

    actualites = Actualite.query.order_by(Actualite.date_publication.desc()).all()
    return render_template('actualites/admin_actualites.html', form=form, actualites=actualites)
