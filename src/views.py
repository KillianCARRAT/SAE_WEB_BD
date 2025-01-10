from .app import app, db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from flask import render_template, redirect, url_for, request, send_from_directory
from datetime import datetime
from hashlib import sha256
from flask_security import Security, SQLAlchemySessionUserDatastore
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from functools import wraps
from flask import abort

#Les imports des formulaires
from .forms.UtilisateurForms import InscriptionForm, ConnexionForm, UpdateUser, UpdatePassword
from .forms.ReservationForms import AjoutSeance

#Les imports des modèles
from .models.Utilisateur import Utilisateur
from .models.Role import Role
from .models.Seance import Seance

def roles(*roles):
    """Vérifie si l'utilisateur a un rôle parmi ceux passés en paramètre
    
    Args:
        *roles : Les rôles à vérifier
        
    Returns:
        decorator : La fonction décorée
    Examples:
        >>> @roles("Administrateur","Organisateur")
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
    f = InscriptionForm()
    f.role.choices =[(role.id_role, role.name) for role in Role.query.all()]
    if f.validate_on_submit():
        if f.validate():
            u = Utilisateur()
            u.nom_utilisateur = f.nom_user.data
            u.prenom_utilisateur = f.prenom_user.data
            u.mdp_utilisateur = sha256(f.mot_de_passe.data.encode()).hexdigest()
            u.email_utilisateur = f.email.data
            u.img_utilisateur = str(Utilisateur.get_last_id()+1)
            u.role_id = f.role.data
            file = f.img.data
            if file:
                if not os.path.exists("src/static/img/profil"):
                    os.makedirs("src/static/img/profil")
                file.save(os.path.join("src/static/img/profil", str(Utilisateur.get_last_id()+1)))
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('login'))
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
@roles("Administrateur","Organisateur")
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
@roles("Administrateur", "Organisateur")
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
            file = f.img.data
            if file:
                file_path = os.path.join("src/static/img/profil", str(current_user.id_utilisateur))
                file.save(file_path)
            db.session.commit()
            return redirect(url_for('home'))
    f.nom_user.data = current_user.nom_utilisateur
    f.prenom_user.data = current_user.prenom_utilisateur
    f.email.data = current_user.email_utilisateur 
    return render_template('profil.html', form=f)

@app.route('/home/ajout_seance', methods=['GET','POST'])
@login_required
@roles("Administrateur","Organisateur")
def ajout_seance():
    """Renvoie la page d'ajout de séance

    Returns:
        ajout_seance.html: Une page d'ajout de séance
    """
    f = AjoutSeance()
    f.moniteur_id.choices = [(user.id_utilisateur, user.nom_utilisateur + " " + user.prenom_utilisateur) for user in Utilisateur.query.all()] # ! Filtrer les moniteurs
    f.moniteur_id.data = current_user.id_utilisateur
    if f.validate_on_submit():
        seance = Seance()
        seance.jour_seance = f.jour_seance.data
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
@roles("Administrateur","Organisateur")
def voir_seances():
    """Renvoie la page de visualisation des séances

    Returns:
        voir_seances.html: Une page de visualisation des séances
    """
    seances = Seance.query.all()
    planning = [[] for i in range(7)]
    for seance in seances:
        planning[seance.jour_seance-1].append(seance)
    print(planning)
    return render_template('seances.html', les_seances=planning)
