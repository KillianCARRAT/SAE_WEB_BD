import click
from .app import app, db
from .models.Utilisateur import Utilisateur
from .models.Role import Role
from hashlib import sha256


@app.cli.command()
def syncdb():
    '''Synchronizes the database.'''
    db.drop_all()
    db.create_all()

    r = Role()
    r.name = "Moniteur"

    r2 = Role()
    r2.name = "Administrateur"

    r3 = Role()
    r3.name = "Client"

    u = Utilisateur()
    u.prenom_utilisateur = "a"
    u.nom_utilisateur = "a"
    u.tel_utilisateur = "0680241926"
    u.poids_utilisateur = "50000"
    u.mdp_utilisateur = sha256("a".encode()).hexdigest()
    u.email_utilisateur = "a"
    u.role_id = 2

    db.session.add(r)
    db.session.add(r2)
    db.session.add(r3)
    db.session.add(u)
    db.session.commit()