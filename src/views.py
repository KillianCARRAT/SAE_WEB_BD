from .app import app, db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from flask import render_template, redirect, url_for, request, send_from_directory
from datetime import datetime
from datetime import timedelta
from hashlib import sha256
from flask_security import Security, SQLAlchemySessionUserDatastore
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from functools import wraps
from flask import abort
from flask import jsonify
from sqlalchemy import or_


#Les imports des formulaires
from .forms.UtilisateurForms import InscriptionForm, ConnexionForm, UpdateUser, UpdatePassword, InscriptionFormAdmin
from .forms.ReservationForms import AjoutSeance
from .forms.ContactForms import ContactForm
from .forms.PoneyForm import PoneyForm

#Les imports des modèles
from .models.Reservation_Utilisateur import Reservation_Utilisateur
from .models.Poney import Poney
from .models.Reservation_Seance import Reservation_Seance
from .models.Reservation import Reservation
from .models.Utilisateur import Utilisateur
from .models.Role import Role
from .models.Seance import Seance
from .models.Contact import Contact
from .models.Date import DateUtils
from .models.Poney import Poney


def roles(*roles):
    """Vérifie si l'utilisateur a un rôle parmi ceux passés en paramètre
    
    Args:
        *roles : Les rôles à vérifier
        
    Returns:
        decorator : La fonction décorée
    Examples:
        >>> @roles("Administrateur","Moniteur")
        >>> def home():
        >>>     return render_template('home.html')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not Role.query.get(current_user.role_id).name in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    """Renvoie la page de connexion

    Returns:
        connexion.html : Une page de connexion
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    f = ConnexionForm()
    if f.validate_on_submit():
        u = f.get_authenticated_user()
        if u:
            login_user(u)
            return redirect(url_for('home'))
    return render_template('connexion.html', form=f)


@app.route('/signin', methods=['GET','POST'])
def signin():
    if current_user.is_authenticated and current_user.is_admin():
        f = InscriptionFormAdmin()
        f.role.choices = [(role.id_role, role.name) for role in Role.query.all()]
    else:
        f = InscriptionForm()
    print("la")
    if f.validate_on_submit():
        print("la")
        if f.validate():
            print("la")
            u = Utilisateur()
            u.nom_utilisateur = f.nom_user.data
            u.prenom_utilisateur = f.prenom_user.data
            u.mdp_utilisateur = sha256(f.mot_de_passe.data.encode()).hexdigest()
            u.email_utilisateur = f.email.data
            if current_user.is_authenticated and current_user.is_admin():
                u.role_id = f.role.data
            else:
                u.role_id = 3
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('login'))
    if current_user.is_authenticated and current_user.is_admin():
        return render_template('signin_admin.html', form=f)
    return render_template('signin.html', form=f)

@app.route('/logout')
@login_required
def logout():
    """Déconnecte l'utilisateur

    Returns:
        login : Redirige vers la page de connexion
    """
    logout_user()
    return redirect(url_for('login'))


# A charger après la définition de la route login
user_datastore = SQLAlchemySessionUserDatastore(db.session, Utilisateur, Role)
security = Security(app, user_datastore)

@app.route('/home', methods=['GET','POST'])
@login_required
@roles("Administrateur","Client","Moniteur")
def home():
    """Renvoie la page d'accueil

    Returns:
        home.html: Une page d'accueil
    """
    return render_template('home.html')


@app.route('/mdp-oublie') # TODO : A faire -> le form et les interactions avec la base de données
def mdp_oublie():
    """Renvoie la page du mot de passe oublié

    Returns:
        mdp-oublie.html : Une page demandant de rentrer son adresse mail pour réinitialiser le mot de passe
    """
    return render_template('mdp-oublie.html')

@app.route('/mdp-reset') # TODO : A faire -> le form et les interactions avec la base de données
def mdp_reset():
    """Renvoie la page de réinitialisation du mot de passe

    Returns:
        mdp-reset.html: Une page pour réinitialiser le mot de passe
    """
    return render_template('mdp-reset.html')

@app.route('/mdp-modif', methods=['GET','POST'])
@login_required
@roles("Administrateur", "Moniteur")
def mdp_modif():
    f = UpdatePassword()
    if f.validate_on_submit():
        if f.validate():
            user = current_user
            user.mdp_utilisateur = sha256(f.new_password.data.encode()).hexdigest()
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('mdp-modif.html', form = f)

@app.route('/home/profil', methods=['GET','POST'])
def modifier_profil():
    """Renvoie la page de modification du profil

    Returns:
        profil.html: Une page de modification du profil
    """
    f = UpdateUser()
    if f.validate_on_submit():
        if f.validate():
            user = current_user  # Récupérer l'utilisateur actuel via Flask-Login
            user.prenom_utilisateur = f.prenom_user.data
            user.nom_utilisateur = f.nom_user.data
            user.email_utilisateur = f.email.data
            db.session.commit()
            return redirect(url_for('home'))
    f.nom_user.data = current_user.nom_utilisateur
    f.prenom_user.data = current_user.prenom_utilisateur
    f.email.data = current_user.email_utilisateur 
    return render_template('profil.html', form=f)

@app.route('/home/ajout_seance', methods=['GET','POST'])
@login_required
@roles("Administrateur","Moniteur")
def ajout_seance():
    """Renvoie la page d'ajout de séance

    Returns:
        ajout_seance.html: Une page d'ajout de séance
    """
    f = AjoutSeance()
    f.moniteur_id.choices = [(user.id_utilisateur, user.nom_utilisateur + " " + user.prenom_utilisateur) for user in Utilisateur.query.filter(Utilisateur.role_id==3)]
    f.moniteur_id.data = current_user.id_utilisateur
    if f.validate_on_submit():
        if f.hebdomadaire_seance.data:
            print("hebdo")
            date_debut = f.date_debut_seance.data
            date_fin = f.date_fin_seance.data
            jour_seance = f.jour_seance.data
            print(date_debut, date_fin, jour_seance)
            date = date_debut
            while date <= date_fin:
                if (date.weekday()+1) == jour_seance:
                    seance = Seance()
                    seance.annee_seance = date.year
                    seance.semaine_seance = date.isocalendar()[1]
                    seance.jour_seance = jour_seance
                    seance.heure_debut_seance = f.heure_debut_seance.data
                    seance.heure_fin_seance = f.heure_fin_seance.data
                    seance.nb_places_seance = f.nb_places_seance.data
                    seance.moniteur_id = f.moniteur_id.data
                    db.session.add(seance)
                date += timedelta(days=1)
        else:
            date = f.semaine_seance.data
            seance = Seance()
            seance.annee_seance = date.year
            seance.semaine_seance = date.isocalendar()[1]
            seance.jour_seance = date.weekday()+1
            seance.heure_debut_seance = f.heure_debut_seance.data
            seance.heure_fin_seance = f.heure_fin_seance.data
            seance.nb_places_seance = f.nb_places_seance.data
            seance.moniteur_id = f.moniteur_id.data
            db.session.add(seance)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('ajout_seance.html', form=f)

@app.route('/home/voir_seances', methods=['GET','POST'])
@login_required
@roles("Administrateur","Moniteur")
def voir_seances():
    """Renvoie la page de visualisation des séances

    Returns:
        voir_seances.html: Une page de visualisation des séances
    """
    return render_template('seances.html')

@app.route('/home/contacter', methods=['GET','POST'])
def contacter():
    """Renvoie la page de contacte d'administrateur/moniteurs

    Returns:
        contacter.html: Une page de contacte d'administrateur/moniteurs
    """
    f = ContactForm()
    if f.validate_on_submit:
        if f.validate():
            c = Contact()
            c.concerne = f.concerne.data
            c.sujet = f.sujet.data
            c.contenu = f.contenu.data
            c.utilisateur = current_user
            c.id_utilisateur = current_user.id_utilisateur
            db.session.add(c)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('contacter.html', form = f)


@app.route('/seances/', methods=['GET','POST'], defaults={'annee':None,'semaine': None})
@app.route('/seances/<int:annee>/<int:semaine>', methods=['GET','POST'])
def seances(annee,semaine):
    if semaine == None or annee == None:
        annee = datetime.now().year
        semaine = datetime.now().isocalendar()[1]
    print(annee, semaine)
    Seances = Seance.query.filter_by(annee_seance=annee, semaine_seance=semaine).all()
    agenda = [[] for _ in range(6)]
    for seance in Seances:
        jour = seance.jour_seance
        seance_dict = {
            "id_seance": seance.id_seance,
            "heure_debut_seance": seance.heure_debut_seance.strftime('%H:%M:%S'),
            "heure_fin_seance": seance.heure_fin_seance.strftime('%H:%M:%S'),
            "nb_places_seance": seance.nb_places_seance,
            "moniteur_id": seance.moniteur_id,
            "active": seance.active == 1
        }
        agenda[jour-1].append(seance_dict)
    print(agenda)
    return jsonify(agenda)

@app.route('/home/seance/<int:id_seance>', methods=['GET','POST'])
def seance(id_seance):
    seance = Seance.query.get(id_seance)
    print(seance.annee_seance, seance.semaine_seance, seance.jour_seance)
    moniteur = Utilisateur.query.get(seance.moniteur_id)
    date = DateUtils.getDate(seance.jour_seance, seance.semaine_seance, seance.annee_seance)
    return render_template('seance.html', seance=seance, moniteur=moniteur, date=date)

@app.route('/home/ajout_poney', methods=['GET','POST'])
@login_required
@roles("Administrateur","Moniteur")

def ajout_poney():
    f = PoneyForm()
    if f.validate_on_submit():
        p = Poney()
        p.nom_poney = f.nom.data
        p.capacite_poney = f.capacite.data
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('ajout_poney.html', form=f)

@app.route('/home/voir_poneys', methods=['GET','POST'])
@login_required
@roles("Administrateur","Moniteur")
def voir_poneys():
    poneys = Poney.query.all()
    return render_template('les_poney.html', poneys=poneys)
  
@app.route('/home/poney/<int:id_poney>', methods=['GET','POST'])
@login_required
@roles("Administrateur","Moniteur")
def poney(id_poney):
    poney = Poney.query.get(id_poney)
    form = PoneyForm()
    form.nom.data = poney.nom_poney
    form.capacite.data = poney.capacite_poney
    if form.validate_on_submit():
        poney.nom_poney = form.nom.data
        poney.capacite_poney = form.capacite.data
        db.session.commit()
        return redirect(url_for('voir_poneys'))
    return render_template('poney.html', poney=poney, form=form)

@app.route('/home/del/poney/<int:id_poney>', methods=['GET','POST'])
@login_required
@roles("Administrateur","Moniteur")
def del_poney(id_poney):
    poney = Poney.query.get(id_poney)
    db.session.delete(poney)
    db.session.commit()
    return redirect(url_for('voir_poneys'))

@app.route('/home/voir_utilisateurs', methods=['GET','POST'])
@login_required
@roles("Administrateur")
def voir_utilisateurs():
    """Renvoie la page de visualisation des Clients et Moniteurs"""
    utilisateurs = Utilisateur.query.filter(or_(Utilisateur.role_id == 1, Utilisateur.role_id == 3)).all()    
    return render_template('les_utilisateurs.html', utilisateurs=utilisateurs)

@app.route('/home/visualiser_seance', methods=['GET','POST'])
def visualiser_seance():
    return render_template('visualiser_seance.html', seances=Seance.query.all())

@app.route('/home/page_seance/<int:id_seance>', methods=['GET','POST'])
def page_seance(id_seance):
    return render_template('page_seance.html', id_seance=id_seance, seance=Seance.query.get(id_seance))

@app.route('/home/inscrire/<int:id_seance>', methods=['GET','POST'])
def inscrire_cours(id_seance):
    seance = Seance.query.get(id_seance)
    user = current_user

    poney = Poney.getPoney(user.poids_utilisateur, seance)

    res = Reservation()
    res.id_poney = poney.id_poney
    res.id_utilisateur = user.id_utilisateur
    db.session.add(res)
    db.session.commit()

    res_u = Reservation_Utilisateur()
    res_u.id_reservation = res.id_reservation
    res_u.id_utilisateur = user.id_utilisateur

    res_s = Reservation_Seance()
    res_s.id_reservation = res.id_reservation
    res_s.id_seance = seance.id_seance

    db.session.add(res_u)
    db.session.add(res_s)
    db.session.commit()
    return redirect(url_for("home"))

