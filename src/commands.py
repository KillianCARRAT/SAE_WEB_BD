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

    db.session.add(r)
    db.session.add(r2)
    db.session.add(r3)
    db.session.commit()