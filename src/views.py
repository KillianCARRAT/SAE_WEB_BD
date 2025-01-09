from .app import app, db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, roles_required,  logout_user, login_user
from flask import render_template, redirect, url_for, request, send_from_directory

from datetime import datetime
from hashlib import sha256
from flask_security import Security, SQLAlchemySessionUserDatastore

from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from functools import wraps
from flask import abort

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